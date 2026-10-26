from pathlib import Path
from fastapi import FastAPI  # for making model url
from pydantic import BaseModel, Field # for validation
import joblib

MODEL_PATH = Path("models/iris_random_forest_model.joblib")
model = joblib.load(MODEL_PATH)

app = FastAPI(title="Iris Random Forest API")

class IrisInput(BaseModel):  # we get four features from the user model
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)

@app.get("/") # at server localhost:8000/
def ready_to_serve():
    return {"status": "Ready to Serve"}

@app.get("/health") # at server localhost:8000/health
def health_check():
    return {"status": "healthy"}

# Endpoint for making predictions with the Iris Random Forest model
@app.post("/predict")
def predict(data: IrisInput):
    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]] # nested list because model expects 2D array
    prediction = int(model.predict(features)[0]) 
    return  {
        "prediction": prediction,
        "class_name": ["setosa", "versicolor", "virginica"][prediction]  # map prediction to class name
    }