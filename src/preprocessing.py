import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os

def load_data(filepath):
    # Some categorical columns have 'NA' strings that mean 'None'
    return pd.read_csv(filepath, keep_default_na=False, na_values=[''])

def preprocess_data(df):
    # Drop Id as it's not a predictor
    if "Id" in df.columns:
        df = df.drop("Id", axis=1)
        
    # Separate features and target
    X = df.drop("SalePrice", axis=1)
    y = df["SalePrice"]
    
    # Identify numerical and categorical columns
    num_cols = X.select_dtypes(include=['float64', 'int64']).columns
    cat_cols = X.select_dtypes(include=['object']).columns
    
    # Preprocessing pipelines
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer([
        ('num', num_pipeline, num_cols),
        ('cat', cat_pipeline, cat_cols)
    ])
    
    X_processed = preprocessor.fit_transform(X)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test, preprocessor

if __name__ == "__main__":
    filepath = os.path.join(os.path.dirname(__file__), "..", "dataset", "train.csv")
    df = load_data(filepath)
    X_train, X_test, y_train, y_test, preprocessor = preprocess_data(df)
    print("Preprocessing completed successfully.")
    print(f"X_train shape: {X_train.shape}")
