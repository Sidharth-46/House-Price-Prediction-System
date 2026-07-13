# 🏠 PriceVision — India House Price Prediction System

An end-to-end machine learning system for predicting house prices across India, built with Flask, React, and scikit-learn.

## 🌟 Overview

PriceVision analyzes **250,000+ property listings** across **20 states** and **42 cities** in India using **Multiple Linear Regression** to predict house prices based on property characteristics.

**Dataset**: [India House Price Prediction](https://www.kaggle.com/datasets/ankushpanday1/india-house-price-prediction) by Ankush Panday

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **ML** | Python, scikit-learn, Pandas, NumPy |
| **Backend** | Flask, Flask-CORS |
| **Frontend** | React.js, Vite |
| **Serialization** | Joblib |
| **Visualization** | Matplotlib, Seaborn |

## 📁 Project Structure

```
HousePricePrediction/
├── app.py                  # Flask backend (API server)
├── requirements.txt        # Python dependencies
├── dataset/
│   ├── india_housing_prices.csv   # 250K property records
│   └── data_description.txt
├── src/
│   ├── preprocessing.py    # Data cleaning & feature engineering
│   ├── train.py            # Model training functions
│   ├── evaluate.py         # Model evaluation & metrics export
│   └── data_setup.py       # Dataset validation
├── notebooks/
│   └── eda.py              # Exploratory Data Analysis
├── models/                 # Generated: trained model + preprocessor
├── frontend/               # React.js application
│   ├── src/
│   │   ├── pages/          # Home, Predict, Dashboard, About
│   │   ├── components/     # Navbar, Footer, Toast
│   │   ├── context/        # ToastContext
│   │   └── services/       # API service layer
│   └── index.html
├── images/                 # EDA visualizations
└── reports/                # Documentation
```

## 🚀 How to Run

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the Model

```bash
python src/evaluate.py
```

This trains the Linear Regression model (+ Decision Tree and Random Forest for comparison), saves:
- `models/linear_regression_model.joblib`
- `models/preprocessor.joblib`
- `models/metrics.json`
- `models/feature_metadata.json`

### 3. Start the Flask Backend

```bash
python app.py
```

The API server starts at `http://localhost:5000`.

### 4. Start the React Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend starts at `http://localhost:5173`.

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/metrics` | Model performance metrics (R², MAE, MSE, RMSE) |
| `GET` | `/api/features` | Feature options for the prediction form |
| `POST` | `/api/predict` | Predict house price from input features |

## 📊 Model Metrics

Evaluated on 50,000 test samples:

| Model | R² | MAE (₹ Lakhs) | RMSE (₹ Lakhs) |
|---|---|---|---|
| **Linear Regression** (Primary) | -0.0002 | 122.32 | 141.21 |
| Decision Tree | -1.0482 | 165.13 | 202.07 |
| Random Forest | -0.0150 | 122.94 | 142.25 |

> **Note**: The low R² scores reflect the synthetic nature of this Kaggle dataset, where price has near-zero correlation with the available features. The ML pipeline itself is correctly implemented.

## 📝 Reports

- [Project Proposal](reports/proposal.md)
- [Literature Survey](reports/literature_survey.md)
- [Dataset Report](reports/dataset_report.md)
- [EDA Report](reports/eda_report.md)
- [Architecture Document](reports/architecture_document.md)
- [Baseline Model Report](reports/baseline_model_report.md)

## 📄 License

Academic project for MLOps coursework.
