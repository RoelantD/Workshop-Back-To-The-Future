import joblib, json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
import pandas as pd

MODEL_PATH = Path("model/home_result_model.joblib")
SCHEMA_PATH = Path("model/schema.json")

if not MODEL_PATH.exists():
    raise RuntimeError("Model not found. Run `python train.py --data football-results.csv` first.")

pipe = joblib.load(MODEL_PATH)
schema = json.loads(SCHEMA_PATH.read_text()) if SCHEMA_PATH.exists() else None

app = FastAPI(title="HomeResult Inference API", version="1.0.0")

class MatchFeatures(BaseModel):
    features: Dict[str, Any] = Field(..., description="Key-value map of feature columns matching the training data.")

@app.get("/")
def root():
    return {"message": "HomeResult Inference API", "features_expected": schema.get("feature_cols") if schema else None}

@app.post("/predict")
def predict(payload: MatchFeatures):
    if not schema:
        raise HTTPException(400, "schema.json missing; re-run training.")
    row = {col: payload.features.get(col, None) for col in schema["feature_cols"]}
    X = pd.DataFrame([row])
    pred = pipe.predict(X)[0]
    proba = pipe.predict_proba(X)[0].tolist()
    return {"prediction": str(pred), "classes": list(pipe.classes_), "probabilities": proba}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
