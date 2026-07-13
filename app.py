"""
Flask Backend for India House Price Prediction System.
Serves the trained model via REST APIs.

Endpoints:
  GET  /api/health    — Health check
  GET  /api/metrics   — Model performance metrics
  GET  /api/features  — Available feature options for the prediction form
  POST /api/predict   — Predict house price from input features
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import json
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from preprocessing import KNOWN_AMENITIES, engineer_amenities, DROP_COLS, TARGET_COL

# ── App Setup ──────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)  # Allow React frontend (different port) to make requests

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset", "india_housing_prices.csv")

# ── Load model artifacts once at startup ───────────────────────────────────────
model = None
preprocessor = None
feature_metadata = None
dataset_options = None
best_model_name = "Unknown Model"
target_log_transformed = False


def load_artifacts():
    """Load model, preprocessor, metadata, and metrics from disk."""
    global model, preprocessor, feature_metadata, dataset_options, best_model_name, target_log_transformed

    model_path = os.path.join(MODELS_DIR, "primary_model.joblib")
    preprocessor_path = os.path.join(MODELS_DIR, "preprocessor.joblib")
    metadata_path = os.path.join(MODELS_DIR, "feature_metadata.json")
    metrics_path = os.path.join(MODELS_DIR, "metrics.json")

    if not os.path.exists(model_path):
        print("⚠️  Model not found. Run `python src/evaluate.py` first.")
        return False

    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)

    with open(metadata_path, "r") as f:
        feature_metadata = json.load(f)
        
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics_data = json.load(f)
            best_model_name = metrics_data.get("primary_model", "Unknown Model")
            target_log_transformed = metrics_data.get("target_log_transformed", False)

    # Extract unique values from the dataset for form dropdowns
    dataset_options = _extract_feature_options()

    print(f"✅ Model ({best_model_name}) and preprocessor loaded successfully.")
    return True


def _extract_feature_options():
    """
    Read the dataset to extract unique values for categorical features.
    Used to populate dropdown options in the React frontend.
    """
    df = pd.read_csv(DATASET_PATH)
    options = {
        "states": sorted(df["State"].unique().tolist()),
        "cities": sorted(df["City"].unique().tolist()),
        "property_types": sorted(df["Property_Type"].unique().tolist()),
        "furnished_statuses": sorted(df["Furnished_Status"].unique().tolist()),
        "transport_accessibility": sorted(df["Public_Transport_Accessibility"].unique().tolist()),
        "facings": sorted(df["Facing"].unique().tolist()),
        "owner_types": sorted(df["Owner_Type"].unique().tolist()),
        "availability_statuses": sorted(df["Availability_Status"].unique().tolist()),
        "bhk_range": {"min": int(df["BHK"].min()), "max": int(df["BHK"].max())},
        "size_range": {"min": int(df["Size_in_SqFt"].min()), "max": int(df["Size_in_SqFt"].max())},
        "year_built_range": {"min": int(df["Year_Built"].min()), "max": int(df["Year_Built"].max())},
        "floor_range": {"min": int(df["Floor_No"].min()), "max": int(df["Floor_No"].max())},
        "total_floors_range": {"min": int(df["Total_Floors"].min()), "max": int(df["Total_Floors"].max())},
        "amenities": KNOWN_AMENITIES,
        # State → City mapping for cascading dropdowns
        "state_city_map": {
            state: sorted(df[df["State"] == state]["City"].unique().tolist())
            for state in df["State"].unique()
        },
    }
    return options


# ── API Routes ─────────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "message": "India House Price Prediction API is running",
    })


@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    """Return model performance metrics (R², MAE, MSE, RMSE)."""
    metrics_path = os.path.join(MODELS_DIR, "metrics.json")
    if not os.path.exists(metrics_path):
        return jsonify({"error": "Metrics not found. Train the model first."}), 404

    with open(metrics_path, "r") as f:
        metrics = json.load(f)
    return jsonify(metrics)


@app.route("/api/features", methods=["GET"])
def get_features():
    """Return available feature options for the prediction form."""
    if dataset_options is None:
        return jsonify({"error": "Feature options not loaded."}), 500
    return jsonify(dataset_options)


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Accept house features as JSON and return the predicted price.
    """
    if model is None or preprocessor is None:
        return jsonify({"error": "Model not loaded. Train the model first."}), 503

    # ── Validate request ─────────────────────────────────────────────
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    # Required fields — these are the RAW input fields the user provides,
    # NOT the post-engineering columns (has_Playground etc. are generated).
    required_fields = [
        "State", "City", "Property_Type", "BHK", "Size_in_SqFt",
        "Year_Built", "Furnished_Status", "Floor_No", "Total_Floors",
        "Nearby_Schools", "Nearby_Hospitals", "Public_Transport_Accessibility",
        "Parking_Space", "Security", "Amenities", "Facing", "Owner_Type",
        "Availability_Status",
    ]
    missing_fields = [f for f in required_fields if f not in data]

    # Age_of_Property can be computed from Year_Built if missing
    if "Age_of_Property" not in data and "Year_Built" in data:
        data["Age_of_Property"] = 2025 - int(data["Year_Built"])

    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "missing_fields": missing_fields,
        }), 400

    # ── Validate numeric fields ──────────────────────────────────────
    try:
        numeric_validations = {
            "BHK": (1, 10),
            "Size_in_SqFt": (100, 50000),
            "Year_Built": (1900, 2030),
            "Floor_No": (0, 100),
            "Total_Floors": (1, 100),
            "Nearby_Schools": (0, 50),
            "Nearby_Hospitals": (0, 50),
        }
        for field, (min_val, max_val) in numeric_validations.items():
            if field in data:
                val = float(data[field])
                if val < min_val or val > max_val:
                    return jsonify({
                        "error": f"{field} must be between {min_val} and {max_val}.",
                    }), 400
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid numeric value: {str(e)}"}), 400

    # ── Build DataFrame for prediction ───────────────────────────────
    try:
        # Create a single-row DataFrame matching the training schema
        input_df = pd.DataFrame([data])

        # Apply the same amenity engineering as training
        if "Amenities" in input_df.columns:
            input_df = engineer_amenities(input_df)

        # Drop columns that were dropped during training
        input_df = input_df.drop(
            columns=[c for c in DROP_COLS if c in input_df.columns],
            errors="ignore",
        )

        # Remove target column if accidentally included
        if TARGET_COL in input_df.columns:
            input_df = input_df.drop(TARGET_COL, axis=1)

        # Enforce exactly the same feature column order as during training
        expected_cols = feature_metadata["all_feature_columns"]
        
        # Add missing columns with None/NaN if any (e.g. if some engineered feature is missing)
        for col in expected_cols:
            if col not in input_df.columns:
                input_df[col] = np.nan
                
        # Reorder columns
        input_df = input_df[expected_cols]
        
        print("\n--- Processing Prediction Request ---")
        print(f"Model used: {best_model_name}")
        print("Input DataFrame before transform:")
        print(input_df.to_dict(orient="records")[0])
        print("-------------------------------------\n")

        # Transform using the same preprocessor
        X = preprocessor.transform(input_df)
        print("Processed Feature Vector (X) shape:", X.shape)

        # Predict
        raw_prediction = model.predict(X)[0]
        print(f"Raw model output: {raw_prediction}")

        prediction = raw_prediction
        if target_log_transformed:
            prediction = np.expm1(prediction)
            print(f"Prediction after inverse transform (np.expm1): {prediction}")

        # Ensure prediction is non-negative
        prediction = max(0, float(prediction))
        
        result_json = {
            "predicted_price_lakhs": round(prediction, 2),
            "predicted_price_formatted": f"₹ {prediction:,.2f} Lakhs",
            "predicted_price_rupees": f"₹ {prediction * 100000:,.0f}",
            "model_used": best_model_name,
        }
        
        print("Final output sent to frontend:")
        print(json.dumps(result_json, indent=2))
        print("-------------------------------------\n")

        return jsonify(result_json)

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


# ── Error Handlers ─────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found."}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed."}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error."}), 500


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    load_artifacts()
    app.run(debug=True, host="0.0.0.0", port=5001)
