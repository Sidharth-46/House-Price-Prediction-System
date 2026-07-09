# Exploratory Data Analysis (EDA) Report

This document highlights the findings from analyzing the Kaggle Ames Housing Dataset. The generated plots can be found in the `images/` directory.

## Dataset Overview
The dataset contains 1,460 entries with 81 features (mix of numerical and categorical). 

## Missing Value Analysis
A systematic check for nulls revealed that several features have a high proportion of missing values:
- `PoolQC`: 1453 missing
- `MiscFeature`: 1406 missing
- `Alley`: 1369 missing
- `Fence`: 1179 missing
- `MasVnrType`: 872 missing
- `FireplaceQu`: 690 missing
**Action taken**: Features missing primarily represent the absence of the amenity (e.g., no pool). A pipeline using a `most_frequent` imputer combined with robust `OneHotEncoder` handled categorical missingness, while a `median` imputer handled missing numerics (like `LotFrontage`).

## Correlation Heatmap
The correlation heatmap (`images/correlation_heatmap.png`) evaluated linear relationships between the top 10 numeric features and the target variable `SalePrice`.
- `OverallQual` and `GrLivArea` show strong positive correlations with `SalePrice`.
- Features like `GarageCars` and `GarageArea` also show significant correlation, confirming that size and quality are the primary driving factors of value.

## Feature Distributions
The distribution of the target variable, `SalePrice` (`images/target_distribution.png`), reveals:
- A right-skewed normal distribution. Most houses fall in the $100,000 - $250,000 range.
- A long tail of highly expensive homes ($400,000+).

## Outlier Analysis
Using boxplots (`images/income_boxplot.png`), we examined the relationship between `OverallQual` and `SalePrice`:
- Generally, as quality increases, price increases non-linearly.
- There are significant outliers at the higher quality levels, indicating that while quality is a strong predictor, other factors (like neighborhood or specific amenities) also heavily influence the final premium price.

## Insights and Observations
- The dataset's high dimensionality requires solid preprocessing to avoid the curse of dimensionality.
- Tree-based ensemble models like Random Forest are expected to perform exceptionally well given the large number of categorical variables and potential non-linear relationships.
