"""
Model training module for India House Price Prediction.
Provides training functions for baseline models and advanced tuned models.
"""

from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor
import joblib
import os


MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def train_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def train_ridge(X_train, y_train):
    model = Ridge(alpha=1.0, random_state=42)
    model.fit(X_train, y_train)
    return model


def train_lasso(X_train, y_train):
    model = Lasso(alpha=0.1, random_state=42)
    model.fit(X_train, y_train)
    return model


def train_elasticnet(X_train, y_train):
    model = ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42)
    model.fit(X_train, y_train)
    return model


def train_decision_tree(X_train, y_train):
    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    return model


def tune_random_forest(X_train, y_train):
    param_grid = {
        'n_estimators': [50],
        'max_depth': [10],
        'min_samples_split': [5]
    }
    rf = RandomForestRegressor(random_state=42, n_jobs=-1)
    grid_search = GridSearchCV(rf, param_grid, cv=3, scoring='r2', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_


def train_gradient_boosting(X_train, y_train):
    model = GradientBoostingRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model


def tune_gradient_boosting(X_train, y_train):
    param_grid = {
        'n_estimators': [50],
        'learning_rate': [0.1],
        'max_depth': [3]
    }
    gb = GradientBoostingRegressor(random_state=42)
    grid_search = GridSearchCV(gb, param_grid, cv=3, scoring='r2', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_


def train_xgboost(X_train, y_train):
    model = XGBRegressor(random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    return model


def tune_xgboost(X_train, y_train):
    param_grid = {
        'n_estimators': [50],
        'learning_rate': [0.1],
        'max_depth': [3]
    }
    xgb = XGBRegressor(random_state=42, n_jobs=-1)
    grid_search = GridSearchCV(xgb, param_grid, cv=3, scoring='r2', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_


def save_model(model, filename="primary_model.joblib"):
    """Save a trained model to the models/ directory using joblib."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    filepath = os.path.join(MODELS_DIR, filename)
    joblib.dump(model, filepath)
    print(f"✅ Model saved to {filepath}")
    return filepath

