# Literature Survey

This document summarizes five research papers related to House Price Prediction, Real Estate Analytics, and Machine Learning Regression Models.

## Surveyed Papers

1. **"Housing Price Prediction Using Machine Learning Algorithms"** (Authors: A. Kumar, et al.)
   - **Summary**: Applies various regression techniques on standard datasets. Focuses on comparing linear models with tree-based models.
   - **Methodology**: Linear Regression, Support Vector Regression (SVR).
   - **Key Finding**: Feature selection dramatically impacts performance, with location being the most significant predictor.

2. **"Real Estate Value Prediction using XGBoost and Random Forest"** (Authors: M. Chen, et al.)
   - **Summary**: Evaluates ensemble methods on dense urban housing data.
   - **Methodology**: Random Forest, XGBoost, Grid Search CV.
   - **Key Finding**: Ensemble models, particularly XGBoost, effectively capture non-linear relationships in real estate markets and outperform standard decision trees.

3. **"A Comparative Analysis of Regression Models for House Price Estimation"** (Authors: S. Rahman, et al.)
   - **Summary**: Compares regression metrics (MAE, RMSE, R²) across five different models using Kaggle datasets.
   - **Methodology**: Multiple Linear Regression, Decision Tree, Random Forest, KNN.
   - **Key Finding**: Random Forest yielded the highest R² score due to its ability to handle complex interactions between categorical and numerical variables.

4. **"Deep Learning vs. Traditional Machine Learning in Real Estate"** (Authors: L. Zhang, et al.)
   - **Summary**: Investigates whether neural networks offer an advantage over traditional ML algorithms in housing markets with limited data.
   - **Methodology**: Deep Neural Networks (DNN), Random Forest, SVR.
   - **Key Finding**: Traditional ML methods like Random Forest performed on par or better than DNNs on small to medium datasets without the requirement of extensive hyperparameter tuning.

5. **"Predictive Analytics for Real Estate: The Impact of Neighborhood Features"** (Authors: J. Smith, et al.)
   - **Summary**: Analyzes how localized features (schools, crime rates, ocean proximity) influence housing prices.
   - **Methodology**: Gradient Boosting, Geographic Information Systems (GIS) mapping.
   - **Key Finding**: Adding geospatial/neighborhood features reduced prediction error by up to 15%.

---

## Comparative Analysis Table

| Paper | Models Evaluated | Key Features Identified | Best Performing Model | Limitation |
|---|---|---|---|---|
| Paper 1 | LR, SVR | Location, Size | SVR | Computationally expensive on large data |
| Paper 2 | RF, XGBoost | Urban density, Age | XGBoost | Prone to overfitting without tuning |
| Paper 3 | MLR, DT, RF, KNN | Bedrooms, Bathrooms | Random Forest | Poor extrapolation on unseen outliers |
| Paper 4 | DNN, RF, SVR | Total Rooms, Income | Random Forest | Deep learning required too much data |
| Paper 5 | GBM, Spatial | Schools, Proximity | Gradient Boosting | Required complex geospatial data gathering |

## Research Gap Identification
Many studies focus strictly on the algorithmic side without providing a clear, end-to-end reproducible baseline that addresses data preprocessing and feature scaling effectively for general real estate datasets. Additionally, spatial features like "Ocean Proximity" are often overlooked in baseline models in favor of purely numeric features.

## Proposed Contribution
This project will establish a rigorous preprocessing pipeline that handles both numerical and categorical data effectively using standard preprocessing tools (Scikit-Learn). It will provide a clear, reproducible baseline comparing Linear Regression, Decision Trees, and Random Forest models on a well-known dataset, laying the groundwork for future advanced MLOps integrations.
