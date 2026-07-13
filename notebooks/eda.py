"""
Exploratory Data Analysis for India Housing Prices dataset.
Generates visualizations and saves them to the images/ directory.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Consistent plot styling
sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.dpi"] = 120


def run_eda():
    filepath = os.path.join(os.path.dirname(__file__), "..", "dataset", "india_housing_prices.csv")
    images_dir = os.path.join(os.path.dirname(__file__), "..", "images")
    os.makedirs(images_dir, exist_ok=True)

    print("📂 Loading dataset...")
    df = pd.read_csv(filepath)
    print(f"   Shape: {df.shape}\n")

    # ── 1. Dataset overview ──────────────────────────────────────────
    print("Dataset Head:")
    print(df.head())

    # ── 2. Missing value analysis ────────────────────────────────────
    print("\nMissing Values:")
    missing = df.isnull().sum()
    missing_nonzero = missing[missing > 0]
    if missing_nonzero.empty:
        print("  No missing values found! ✅")
    else:
        print(missing_nonzero.sort_values(ascending=False).head(10))

    # ── 3. Correlation heatmap (top 10 features vs Price_in_Lakhs) ──
    plt.figure(figsize=(12, 10))
    numeric_df = df.select_dtypes(include=["float64", "int64"])
    if "ID" in numeric_df.columns:
        numeric_df = numeric_df.drop("ID", axis=1)
    corr = numeric_df.corr()
    top_corr = corr["Price_in_Lakhs"].abs().sort_values(ascending=False).head(10).index
    sns.heatmap(numeric_df[top_corr].corr(), annot=True, cmap="coolwarm", fmt=".2f",
                linewidths=0.5, square=True)
    plt.title("Correlation Heatmap — Top 10 Features vs Price_in_Lakhs", fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "correlation_heatmap.png"))
    plt.close()
    print("\n📊 Saved: correlation_heatmap.png")

    # ── 4. Target variable distribution ──────────────────────────────
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Price_in_Lakhs"], bins=60, kde=True, color="#4361ee")
    plt.title("Distribution of Price (in Lakhs)", fontsize=14)
    plt.xlabel("Price (₹ Lakhs)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "target_distribution.png"))
    plt.close()
    print("📊 Saved: target_distribution.png")

    # ── 5. BHK vs Price boxplot ──────────────────────────────────────
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df["BHK"], y=df["Price_in_Lakhs"], palette="viridis")
    plt.title("BHK vs Price (in Lakhs)", fontsize=14)
    plt.xlabel("BHK")
    plt.ylabel("Price (₹ Lakhs)")
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "bhk_price_boxplot.png"))
    plt.close()
    print("📊 Saved: bhk_price_boxplot.png")

    # ── 6. Property Type distribution ────────────────────────────────
    plt.figure(figsize=(8, 6))
    df["Property_Type"].value_counts().plot(kind="bar", color=["#4361ee", "#3a0ca3", "#7209b7"])
    plt.title("Property Type Distribution", fontsize=14)
    plt.xlabel("Property Type")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "property_type_distribution.png"))
    plt.close()
    print("📊 Saved: property_type_distribution.png")

    # ── 7. Top 10 cities by average price ────────────────────────────
    plt.figure(figsize=(12, 6))
    city_avg = df.groupby("City")["Price_in_Lakhs"].mean().sort_values(ascending=False).head(10)
    city_avg.plot(kind="barh", color="#4361ee")
    plt.title("Top 10 Cities by Average House Price", fontsize=14)
    plt.xlabel("Average Price (₹ Lakhs)")
    plt.ylabel("City")
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "top_cities_price.png"))
    plt.close()
    print("📊 Saved: top_cities_price.png")

    print("\n✅ EDA completed. All images saved to the 'images/' directory.")


if __name__ == "__main__":
    run_eda()
