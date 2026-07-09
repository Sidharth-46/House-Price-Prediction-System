import os
import pandas as pd
import urllib.request

def download_data():
    url = "https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.csv"
    data_path = os.path.join("..", "dataset", "housing.csv")
    
    print(f"Downloading dataset from {url}...")
    urllib.request.urlretrieve(url, data_path)
    print(f"Dataset downloaded and saved to {data_path}")

    # Load and show info
    df = pd.read_csv(data_path)
    print("\nDataset Info:")
    print(df.info())

if __name__ == "__main__":
    download_data()
