"""
Preprocessing module for India Housing Prices dataset.
Handles data loading, cleaning, feature engineering, and train/test splitting.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os
import json


# ── Constants ──────────────────────────────────────────────────────────────────
DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "india_housing_prices.csv")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

TARGET_COL = "Price_in_Lakhs"

# Columns to drop: ID is an identifier, Price_per_SqFt is derived from
# the target (data leakage), Locality has 500+ unique values (too sparse)
DROP_COLS = ["ID", "Price_per_SqFt", "Locality", "Realistic_Price_per_SqFt"]

# Known amenities that can appear in the Amenities column
KNOWN_AMENITIES = ["Playground", "Gym", "Garden", "Pool", "Clubhouse"]


def load_data(filepath=None):
    """Load the India Housing Prices CSV dataset."""
    if filepath is None:
        filepath = DATASET_PATH
    df = pd.read_csv(filepath)
    return df


def engineer_amenities(df):
    """
    Convert the 'Amenities' column (comma-separated string) into
    binary indicator columns: has_Playground, has_Gym, etc.
    Then drop the original Amenities column.
    """
    for amenity in KNOWN_AMENITIES:
        col_name = f"has_{amenity}"
        df[col_name] = df["Amenities"].str.contains(amenity, case=False, na=False).astype(int)
    df = df.drop("Amenities", axis=1)
    return df


def remove_outliers_iqr(df, column):
    """Remove outliers from a numeric column using the IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]


def preprocess_data(df, save_artifacts=True):
    """
    Full preprocessing pipeline:
    1. Remove invalid records (e.g., Floor_No > Total_Floors)
    2. Remove outliers using IQR method
    3. Drop unnecessary columns (ID, Price_per_SqFt, Locality)
    4. Engineer amenity binary features from the Amenities string
    5. Separate features (X) and target (y)
    6. Build sklearn ColumnTransformer pipeline:
       - Numerical: median imputation → StandardScaler
       - Categorical: most-frequent imputation → OneHotEncoder
    7. Fit-transform X, split into train/test
    8. Optionally save the preprocessor + feature metadata to models/

    Returns:
        X_train, X_test, y_train, y_test, preprocessor
    """
    # Step 1: Remove invalid records
    initial_len = len(df)
    df = df[((df["Floor_No"] <= df["Total_Floors"]) | (df["Total_Floors"] == 0))]
    df = df[df["Size_in_SqFt"] > 0]
    
    # Step 2: Remove outliers using IQR
    df = remove_outliers_iqr(df, "Size_in_SqFt")
    if TARGET_COL in df.columns:
        df = remove_outliers_iqr(df, TARGET_COL)
    
    print(f"🧹 Removed {initial_len - len(df)} invalid/outlier records.")

    # Step 3: Drop columns
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns], errors="ignore")

    # Step 4: Engineer amenity features
    if "Amenities" in df.columns:
        df = engineer_amenities(df)

    # Step 5: Separate features and target
    X = df.drop(TARGET_COL, axis=1)
    y = df[TARGET_COL]

    # Identify column types
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(include=["object", "string"]).columns.tolist()
    
    # Explicitly reorder columns to ensure consistency
    X = X[num_cols + cat_cols]

    # Step 6: Build preprocessing pipelines
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer([
        ("num", num_pipeline, num_cols),
        ("cat", cat_pipeline, cat_cols),
    ])

    # Step 7: Fit and transform
    X_processed = preprocessor.fit_transform(X)

    # Step 8: Train/test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, random_state=42
    )

    # Step 9: Save artifacts
    if save_artifacts:
        os.makedirs(MODELS_DIR, exist_ok=True)

        # Save the fitted preprocessor
        joblib.dump(preprocessor, os.path.join(MODELS_DIR, "preprocessor.joblib"))

        # Save feature metadata so the Flask API knows what columns to expect
        feature_metadata = {
            "numerical_columns": num_cols,
            "categorical_columns": cat_cols,
            "all_feature_columns": num_cols + cat_cols,
            "target_column": TARGET_COL,
            "drop_columns": DROP_COLS,
            "known_amenities": KNOWN_AMENITIES,
        }
        with open(os.path.join(MODELS_DIR, "feature_metadata.json"), "w") as f:
            json.dump(feature_metadata, f, indent=2)

        print(f"✅ Preprocessor saved to {MODELS_DIR}/preprocessor.joblib")
        print(f"✅ Feature metadata saved to {MODELS_DIR}/feature_metadata.json")

    return X_train, X_test, y_train, y_test, preprocessor


# ── CLI Entry Point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_data()
    X_train, X_test, y_train, y_test, preprocessor = preprocess_data(df)
    print(f"\n📊 Preprocessing completed successfully.")
    print(f"   Training set shape: {X_train.shape}")
    print(f"   Test set shape:     {X_test.shape}")
