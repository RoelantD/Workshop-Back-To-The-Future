# Step-by-Step Workshop: Running and Deploying Your Model (`app.py`)

This guide will show you how to run your trained model locally using the provided FastAPI app, and give you a glimpse of what cloud deployment would look like.

---

## 1. Introduction

After training your model, you can serve it as an API so others (or your own applications) can make predictions. We'll use FastAPI for this purpose.

---

## 2. How the Script Works (`app.py`)

- Loads the trained model (`home_result_model.joblib`) and schema (`schema.json`).
- Starts a FastAPI web server with two endpoints:
	- `GET /` returns a welcome message and the expected feature columns.
	- `POST /predict` accepts a JSON payload with feature values and returns a prediction and probabilities.
- Uses Pydantic for input validation and Pandas for data handling.

**Key code parts:**
```python
pipe = joblib.load(MODEL_PATH)  # Loads the trained model
schema = json.loads(SCHEMA_PATH.read_text()) if SCHEMA_PATH.exists() else None

@app.post("/predict")
def predict(payload: MatchFeatures):
		row = {col: payload.features.get(col, None) for col in schema["feature_cols"]}
		X = pd.DataFrame([row])
		pred = pipe.predict(X)[0]
		proba = pipe.predict_proba(X)[0].tolist()
		return {"prediction": str(pred), "classes": list(pipe.classes_), "probabilities": proba}
```

---

## 3. Running the API Locally

1. Make sure you have trained your model and have `model/home_result_model.joblib` and `model/schema.json`.
2. Install requirements:
	 ```bash
	 pip install -r part-1/code/requirements.txt
	 ```
3. Start the API server:
	 ```bash
	 python part-1/code/app.py
	 ```
4. Open your browser and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to try out the interactive API documentation (Swagger UI).
5. Use the `/predict` endpoint to send a JSON object with your feature values and get a prediction.

---

## 4. Example Prediction Request

Send a POST request to `/predict` with a JSON body like:
```json
{
	"features": {
		"HomeTeam": "TeamA",
		"AwayTeam": "TeamB",
		"Weather": "Rainy",
		"DayOfWeek": "Saturday",
		"Referee": "Smith"
		// ...other features as required by your model
	}
}
```

You can use the Swagger UI or a tool like Postman/curl to test this.

---

## 5. What About Cloud Deployment?

Deploying to the cloud (e.g., Azure, AWS, GCP) usually involves:
- Packaging your app (often with Docker)
- Pushing it to a cloud service (like Azure App Service, AWS Elastic Beanstalk, or Google Cloud Run)
- Setting environment variables and storage for your model files
- Exposing the API endpoint to the internet

The code in `app.py` is already structured for easy deployment—just point your cloud service to run `python app.py` and make sure your model files are available.

---

Find the full code in [`app.py`](./code/app.py).

[⏮️ Previous](/part-1/1-9-train-model.md) 
[⏭️ Next](/part-2/2-1-create-vanilla-agent.md)