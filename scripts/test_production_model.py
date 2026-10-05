import joblib
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

model_path = MODELS_DIR / "primary_model.joblib"
preprocessor_path = MODELS_DIR / "preprocessor.joblib"
metadata_path = MODELS_DIR / "feature_metadata.json"
metrics_path = MODELS_DIR / "metrics.json"

print(f"Model path: {model_path}")
print(f"Exists: {model_path.exists()}")
if model_path.exists():
    print(f"Size: {model_path.stat().st_size}")

try:
    model = joblib.load(model_path)
    print(f"Model type: {type(model)}")
    print("SUCCESS")
except Exception as e:
    import traceback
    print("FAILED")
    traceback.print_exc()

print(f"Preprocessor path: {preprocessor_path}")
print(f"Exists: {preprocessor_path.exists()}")
try:
    preprocessor = joblib.load(preprocessor_path)
    print(f"Preprocessor type: {type(preprocessor)}")
    print("SUCCESS")
except Exception as e:
    import traceback
    print("FAILED")
    traceback.print_exc()
