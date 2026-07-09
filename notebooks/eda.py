import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda():
    filepath = os.path.join(os.path.dirname(__file__), "..", "dataset", "train.csv")
    images_dir = os.path.join(os.path.dirname(__file__), "..", "images")
    
    df = pd.read_csv(filepath)
    
    # 1. Dataset overview
    print("Dataset Head:")
    print(df.head())
    
    # 2. Missing value analysis (top 10 missing)
    print("\nTop 10 Missing Values:")
    missing = df.isnull().sum()
    print(missing[missing > 0].sort_values(ascending=False).head(10))
    
    # 3. Correlation heatmap
    plt.figure(figsize=(12, 10))
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    # Plot only top 10 highly correlated features with SalePrice for readability
    top_corr = numeric_df.corr()['SalePrice'].sort_values(ascending=False).head(10).index
    sns.heatmap(df[top_corr].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap (Top 10 Features)')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "correlation_heatmap.png"))
    plt.close()
    
    # 4. Feature distributions (Target variable)
    plt.figure(figsize=(8, 6))
    sns.histplot(df['SalePrice'], bins=50, kde=True)
    plt.title('Distribution of Sale Price')
    plt.xlabel('Sale Price')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "target_distribution.png"))
    plt.close()
    
    # 5. Outlier analysis (Boxplot)
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df['OverallQual'], y=df['SalePrice'])
    plt.title('Outlier Analysis - Overall Quality vs Sale Price')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "income_boxplot.png"))  # Keeping same filename for simplicity
    plt.close()
    
    print("\nEDA completed. Images saved to the 'images' directory.")

if __name__ == "__main__":
    run_eda()
