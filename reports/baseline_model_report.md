# Baseline Machine Learning Models Report

This document compares the performance of three baseline regression models trained to predict `SalePrice` on the Ames Housing Dataset.

## Data Preprocessing Steps Applied
1. **Missing values**: Imputed using `median` for numeric columns and `most_frequent` for categorical columns.
2. **Encoding**: Categorical columns were One-Hot Encoded.
3. **Scaling**: Numerical features were scaled using `StandardScaler` to ensure zero mean and unit variance.
4. **Data Splitting**: The dataset was split into 80% training and 20% testing sets.

## Evaluated Models
1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor

## Performance Evaluation
Metrics were computed on the unseen test set (20% of data).

| Model | MAE | MSE | RMSE | R² Score |
|---|---|---|---|---|
| **Linear Regression** | 23,721.85 | 1,389,154,015.46 | 37,271.36 | 0.8189 |
| **Decision Tree** | 28,362.01 | 1,902,762,384.04 | 43,620.66 | 0.7519 |
| **Random Forest** | 17,667.80 | 851,215,535.03 | 29,175.60 | 0.8890 |

### Metric Explanations
- **MAE (Mean Absolute Error)**: Average absolute difference between predicted and actual prices.
- **MSE (Mean Squared Error)**: Punishes larger errors significantly more.
- **RMSE (Root Mean Squared Error)**: Standard deviation of prediction errors.
- **R² Score**: Proportion of variance in the target explained by the model (1.0 is perfect).

## Conclusion and Model Selection
The **Random Forest Regressor** is the best baseline model. 
- It explains roughly **88.9%** of the variance in house prices, heavily outperforming the Decision Tree (`0.7519`) and significantly improving on Linear Regression (`0.8189`).
- Its MAE is remarkably low at $17,667, demonstrating strong accuracy for a baseline model on the complex Ames dataset.

**Selected Baseline Model: Random Forest Regressor**
