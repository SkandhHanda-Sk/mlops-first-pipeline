# Import TestClient so we can send simulated HTTP requests directly to FastAPI
from fastapi.testclient import TestClient

# Import the application object defined in main.py
from main import app

# Create a reusable TestClient for all test functions.
client = TestClient(app)

# Now we can test the functionality of the API endpoints defined in main.py using the client object.

def test_health_endpoint():
    """
    Verify that the application is running and can respond to a health-check request
    """

    # A successful HTTP request should return status code 200
    response = client.get("/health")
    assert response.status_code == 200 # assert checks if the response status code is 200 (OK), otherwise raise an assertion error

    # Now check response body
    assert response.json() == {"status": "healthy"} # assert checks if the response body is {"status": "healthy"}, otherwise raise an assertion error


def test_valid_iris_prediction():
    """
    Verify that valid flower measurements produce a prediction
    """
    payload = {
        "sepal_length": 3.4,
        "sepal_width": 1.4,
        "petal_length": 3.4,
        "petal_width": 0.4,
    }

    # Send a simulated HTTP POST request with JSON input
    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    # Convert the JSON respnse into a Python Dictionary
    result = response.json()

    # Check the response contract: both fields must exists
    assert "prediction" in result
    assert "class_name" in result

    # The predicted class must be one of the three Iris classes
    assert result["class_name"] in ["setosa", "versicolor", "virginica"]
    # The predicted integer must be between 0 and 2 (inclusive)
    assert result["prediction"] in [0, 1, 2]

def test_invalid_iris_input():
    """
    Verify that invalid flower measurements produce a validation error
    """
    payload = {
        "sepal_length": -3.4,  # Invalid negative value
        "sepal_width": 1.4,
        "petal_length": 3.4,
        "petal_width": 0.4,
    }

    # Send a simulated HTTP POST request with JSON input
    response = client.post("/predict", json=payload)
    # FastAPI returns HTTP 422 for validation errors
    assert response.status_code == 422