"""
Model evaluation module for India House Price Prediction.
Trains all baseline models, evaluates them using CV, saves the best model
and metrics to disk for the Flask API to serve. Also generates plots.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, KFold
import os
import sys
import json
import mlflow
import mlflow.sklearn

# Add src to path to import sibling modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from preprocessing import load_data, preprocess_data, TARGET_COL
from train import (
    train_linear_regression,
    train_ridge,
    train_lasso,
    train_elasticnet,
    train_decision_tree,
    tune_random_forest,
    tune_gradient_boosting,
    tune_xgboost,
    save_model
)


MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")


def evaluate_model(model, X_train, y_train, X_test, y_test, model_name, apply_log):
    """
    Evaluate a trained model using test set and 3-fold CV.
    Returns a dictionary of metrics.
    """
    cv_scores = cross_val_score(model, X_train, y_train, cv=3, scoring='r2', n_jobs=-1)
    cv_mean = cv_scores.mean()

    predictions = model.predict(X_test)
    if apply_log:
        predictions = np.expm1(predictions)

    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)
    
    print(f"--- {model_name} ---")
    print(f"  MAE:  ₹{mae:.2f} Lakhs")
    print(f"  MSE:  {mse:.2f}")
    print(f"  RMSE: ₹{rmse:.2f} Lakhs")
    print(f"  R²:   {r2:.4f}")
    print(f"  CV R²: {cv_mean:.4f}\n")

    return {
        "model_name": model_name,
        "model_obj": model,
        "mae": round(mae, 4),
        "mse": round(mse, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4),
        "cv_r2": round(cv_mean, 4),
        "predictions": predictions
    }


def generate_plots(results_dict, y_test, feature_names):
    """Generate 6 evaluation plots and save them."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    best_result = min(results_dict, key=lambda x: x["rmse"])
    best_model_name = best_result["model_name"]
    best_predictions = best_result["predictions"]
    best_model_obj = best_result["model_obj"]
    residuals = y_test - best_predictions

    # 1. Actual vs Predicted
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, best_predictions, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Price (Lakhs)')
    plt.ylabel('Predicted Price (Lakhs)')
    plt.title(f'{best_model_name}: Actual vs Predicted')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'actual_vs_predicted.png'))
    plt.close()

    # 2. Residual Plot
    plt.figure(figsize=(8, 6))
    plt.scatter(best_predictions, residuals, alpha=0.5)
    plt.axhline(0, color='r', linestyle='--', lw=2)
    plt.xlabel('Predicted Price (Lakhs)')
    plt.ylabel('Residuals')
    plt.title(f'{best_model_name}: Residual Plot')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'residual_plot.png'))
    plt.close()

    # 3. Error Distribution
    plt.figure(figsize=(8, 6))
    sns.histplot(residuals, kde=True, bins=50)
    plt.xlabel('Prediction Error (Lakhs)')
    plt.title(f'{best_model_name}: Error Distribution')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'error_distribution.png'))
    plt.close()
    
    # 4. Feature Importance
    if hasattr(best_model_obj, 'feature_importances_'):
        importances = best_model_obj.feature_importances_
        indices = np.argsort(importances)[-20:]
        plt.figure(figsize=(10, 8))
        plt.title('Feature Importances (Top 20)')
        plt.barh(range(len(indices)), importances[indices], color='b', align='center')
        plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
        plt.xlabel('Relative Importance')
        plt.tight_layout()
        plt.savefig(os.path.join(REPORTS_DIR, 'feature_importance.png'))
        plt.close()
        
    # 5. Prediction Error Histogram
    plt.figure(figsize=(8, 6))
    sns.histplot(np.abs(residuals), kde=True, bins=50, color='orange')
    plt.xlabel('Absolute Prediction Error (Lakhs)')
    plt.title(f'{best_model_name}: Absolute Error Histogram')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'prediction_error_histogram.png'))
    plt.close()
        
    print(f"✅ Evaluation plots saved to {REPORTS_DIR}")


def main():
    print("📂 Loading India Housing Prices dataset...")
    df = load_data()
    print(f"   Dataset shape: {df.shape}\n")
    
    # 6. Correlation Heatmap
    print("📈 Generating Correlation Heatmap...")
    os.makedirs(REPORTS_DIR, exist_ok=True)
    num_df = df.select_dtypes(include=['int64', 'float64'])
    plt.figure(figsize=(12, 10))
    sns.heatmap(num_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'correlation_heatmap.png'))
    plt.close()

    print("⚙️  Preprocessing data...")
    X_train, X_test, y_train, y_test, preprocessor = preprocess_data(df, save_artifacts=True)
    print(f"   Training samples: {X_train.shape[0]}")
    print(f"   Test samples:     {X_test.shape[0]}")
    print(f"   Features:         {X_train.shape[1]}\n")

    # Step 5: Improve Target Variable
    target_skew = y_train.skew()
    print(f"📊 Target Skewness: {target_skew:.4f}")
    apply_log = False
    if target_skew > 1.0:
        print("   Skewness > 1.0. Applying np.log1p transformation to target variable.")
        y_train_model = np.log1p(y_train)
        apply_log = True
    else:
        print("   Skewness <= 1.0. No transformation needed.")
        y_train_model = y_train.copy()

    models_to_train = [
        ("Linear Regression", train_linear_regression),
        ("Ridge Regression", train_ridge),
        ("Lasso Regression", train_lasso),
        ("ElasticNet", train_elasticnet),
        ("Decision Tree", train_decision_tree),
        ("Random Forest (Tuned)", tune_random_forest),
        ("Gradient Boosting (Tuned)", tune_gradient_boosting),
        ("XGBoost (Tuned)", tune_xgboost)
    ]
    
    results = []
    
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("India_House_Price_Prediction")
    mlflow.sklearn.autolog()

    for name, train_func in models_to_train:
        print(f"🏋️  Training {name}...")
        with mlflow.start_run(run_name=name):
            model = train_func(X_train, y_train_model)
            res = evaluate_model(model, X_train, y_train_model, X_test, y_test, name, apply_log)
            
            mlflow.log_metric("custom_rmse", res["rmse"])
            mlflow.log_metric("custom_mae", res["mae"])
            mlflow.log_metric("custom_r2", res["r2"])
            mlflow.log_metric("cv_r2", res["cv_r2"])
            
            results.append(res)
        
    best_result = min(results, key=lambda x: (x['rmse'], x['mae'], -x['r2']))
    best_model_name = best_result['model_name']
    best_model = best_result['model_obj']
    
    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"   RMSE: ₹{best_result['rmse']} Lakhs")
    print(f"   MAE:  ₹{best_result['mae']} Lakhs")
    print(f"   R²:   {best_result['r2']}")
    print(f"   CV R²:{best_result['cv_r2']}")

    print(f"\n💾 Saving {best_model_name} as primary_model.joblib...")
    save_model(best_model, "primary_model.joblib")

    print("\n📈 Generating Evaluation Plots...")
    cat_encoder = preprocessor.named_transformers_['cat'].named_steps['encoder']
    cat_features = cat_encoder.get_feature_names_out(preprocessor.transformers_[1][2])
    num_features = preprocessor.transformers_[0][2]
    all_features = list(num_features) + list(cat_features)
    
    generate_plots(results, y_test, all_features)
    
    os.makedirs(MODELS_DIR, exist_ok=True)
    metrics_path = os.path.join(MODELS_DIR, "metrics.json")
    
    clean_results = []
    for r in results:
        cr = r.copy()
        cr.pop('model_obj')
        cr.pop('predictions')
        cr['model'] = cr.pop('model_name')
        clean_results.append(cr)
        
    metrics_data = {
        "primary_model": best_model_name,
        "training_samples": int(X_train.shape[0]),
        "test_samples": int(X_test.shape[0]),
        "num_features": int(X_train.shape[1]),
        "target_log_transformed": apply_log,
        "results": clean_results,
    }
    with open(metrics_path, "w") as f:
        json.dump(metrics_data, f, indent=2)
    print(f"✅ Metrics saved to {metrics_path}")
    
    print("\n🔍 Validating Sample Predictions from Test Set...")
    np.random.seed(42)
    sample_indices = np.random.choice(X_test.shape[0], 5, replace=False)
    sample_X = X_test[sample_indices]
    sample_y = y_test.iloc[sample_indices].values
    
    sample_preds = best_model.predict(sample_X)
    if apply_log:
        sample_preds = np.expm1(sample_preds)
        
    for i in range(5):
        actual = sample_y[i]
        pred = sample_preds[i]
        diff = abs(actual - pred)
        flag = "🚩 UNREALISTIC" if diff > (0.5 * actual) else "✅ OK"
        print(f"   House {i+1}: Actual: ₹{actual:.2f}L | Predicted: ₹{pred:.2f}L | Diff: ₹{diff:.2f}L {flag}")

    print("\n✅ All models evaluated. Pipeline complete.")


if __name__ == "__main__":
    main()
