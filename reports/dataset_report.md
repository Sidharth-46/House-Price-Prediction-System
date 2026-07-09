# Dataset Report

## Dataset Source
The dataset used is the widely recognized **Kaggle Ames Housing Dataset** ("House Prices - Advanced Regression Techniques"), provided as `train.csv` and `test.csv`.

## Dataset Description
The dataset contains a rich set of 79 explanatory variables describing (almost) every aspect of residential homes in Ames, Iowa. The goal is to predict the final price of each home.

## Feature Descriptions
The dataset has 81 columns, including:
1. **Id**: Identifier for each record.
2. **MSSubClass**: The building class.
3. **MSZoning**: The general zoning classification.
4. **LotArea**: Lot size in square feet.
5. **OverallQual**: Overall material and finish quality.
6. **OverallCond**: Overall condition rating.
7. **YearBuilt**: Original construction date.
8. **GrLivArea**: Above grade (ground) living area square feet.
9. **SalePrice**: The property's sale price in dollars (Target variable).
*(And ~70 other features covering basement details, garage details, roof style, masonry veneer, and neighborhood).*

## Data Statistics
- **Number of Observations**: 1,460 (in the train set)
- **Number of Features**: 79 explanatory features + 1 Target (`SalePrice`) + 1 ID (`Id`)

### Data Quality Assessment
- **Missing Values**: Many features related to optional amenities (like `PoolQC`, `MiscFeature`, `Alley`, `Fence`, `FireplaceQu`) have a high percentage of missing values, indicating the property lacks that amenity rather than being unknown. Other features like `LotFrontage` and `GarageYrBlt` have true missing values.
- **Duplicates**: No duplicate rows based on `Id`.
- **Outliers**: Outliers exist in features like `GrLivArea` (very large houses) and `LotArea`.
- **Categorical Data**: Features range from ordinal scales (e.g., Ex, Gd, TA, Fa, Po) to nominal strings (e.g., Neighborhood).
- **Scaling Requirements**: Large variations in feature magnitudes (e.g., square footage vs. number of rooms) require standardization.
