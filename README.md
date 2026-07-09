# House Price Prediction System - Review I

This repository contains the Phase 1 (Review-I) deliverables for the House Price Prediction System MLOps project.

## Overview
The goal is to accurately estimate house prices using machine learning by analyzing the California Housing Dataset. This repository establishes the data ingestion, preprocessing, EDA, baseline modeling, and core architecture documents.

## Directory Structure
- `dataset/`: Contains the raw housing data.
- `notebooks/`: Contains the EDA script (`eda.py`).
- `src/`: Contains source code for data preparation, model training, and evaluation.
- `reports/`: Contains all required Markdown documentation.
- `images/`: Stores generated plots from EDA.

## How to Run

1. **Install Requirements:**
   Ensure you have the required libraries installed:
   ```bash
   pip install pandas scikit-learn matplotlib seaborn
   ```

2. **Generate EDA Images:**
   ```bash
   python src/notebooks/eda.py
   ```
   *This saves the visualization plots into the `images/` directory.*

3. **Train and Evaluate Models:**
   ```bash
   python src/evaluate.py
   ```
   *This will run the preprocessing pipeline, train the Linear Regression, Decision Tree, and Random Forest models, and output the MAE, MSE, RMSE, and R2 metrics.*

## Status
- **Review-I Delivered**: Complete baseline pipeline and documentation without deployment, APIs, or Docker components.
