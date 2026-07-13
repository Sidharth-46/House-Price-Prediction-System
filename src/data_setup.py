"""
Data setup / validation module for India House Price Prediction.
Validates that the India Housing Prices dataset exists and has the
expected schema.
"""

import os
import pandas as pd


DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "india_housing_prices.csv")

EXPECTED_COLUMNS = [
    "ID", "State", "City", "Locality", "Property_Type", "BHK",
    "Size_in_SqFt", "Price_in_Lakhs", "Price_per_SqFt", "Year_Built",
    "Furnished_Status", "Floor_No", "Total_Floors", "Age_of_Property",
    "Nearby_Schools", "Nearby_Hospitals", "Public_Transport_Accessibility",
    "Parking_Space", "Security", "Amenities", "Facing", "Owner_Type",
    "Availability_Status",
]


def validate_data():
    """
    Check that the India Housing Prices dataset exists and has
    the expected columns. Prints a summary of the data.
    """
    if not os.path.exists(DATASET_PATH):
        print(f"❌ Dataset not found at {DATASET_PATH}")
        print("   Please download from: https://www.kaggle.com/datasets/ankushpanday1/india-house-price-prediction")
        return False

    df = pd.read_csv(DATASET_PATH, nrows=5)
    actual_cols = list(df.columns)
    missing = [c for c in EXPECTED_COLUMNS if c not in actual_cols]

    if missing:
        print(f"❌ Missing columns: {missing}")
        return False

    # Quick stats on full dataset (row count only)
    row_count = sum(1 for _ in open(DATASET_PATH)) - 1  # minus header
    print(f"✅ Dataset validated successfully!")
    print(f"   Path:    {DATASET_PATH}")
    print(f"   Rows:    {row_count:,}")
    print(f"   Columns: {len(actual_cols)}")
    print(f"   Columns: {actual_cols}")
    return True


if __name__ == "__main__":
    validate_data()
