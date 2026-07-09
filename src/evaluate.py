import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import os
import sys

# Add src to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from preprocessing import load_data, preprocess_data
from train import train_linear_regression, train_decision_tree, train_random_forest

def evaluate_model(model, X_test, y_test, model_name):
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)
    
    print(f"--- {model_name} ---")
    print(f"MAE:  {mae:.2f}")
    print(f"MSE:  {mse:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2:   {r2:.4f}\n")
    return {"Model": model_name, "MAE": mae, "MSE": mse, "RMSE": rmse, "R2": r2}

def main():
    filepath = os.path.join(os.path.dirname(__file__), "..", "dataset", "train.csv")
    df = load_data(filepath)
    X_train, X_test, y_train, y_test, preprocessor = preprocess_data(df)
    
    print("Training Linear Regression...")
    lr_model = train_linear_regression(X_train, y_train)
    
    print("Training Decision Tree...")
    dt_model = train_decision_tree(X_train, y_train)
    
    print("Training Random Forest...")
    rf_model = train_random_forest(X_train, y_train)
    
    print("Evaluating Models...\n")
    results = []
    results.append(evaluate_model(lr_model, X_test, y_test, "Linear Regression"))
    results.append(evaluate_model(dt_model, X_test, y_test, "Decision Tree"))
    results.append(evaluate_model(rf_model, X_test, y_test, "Random Forest"))

    print("Baseline Models Evaluation Completed.")

if __name__ == "__main__":
    main()
