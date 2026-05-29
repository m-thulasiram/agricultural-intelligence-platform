import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any


class TestPredictionEndpoints:
    def test_health_endpoint(self, client: TestClient):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Crop Health Forecasting API"
        assert data["version"] == "1.0.0"

    def test_predict_valid_input(
        self, client: TestClient, sample_predict_data: Dict[str, Any]
    ):
        response = client.post("/api/v1/predict", json=sample_predict_data)
        assert response.status_code in (200, 201)
        data = response.json()
        assert "predicted_yield" in data
        assert data["item"] == sample_predict_data["item"]
        assert data["year"] == sample_predict_data["Year"]

    def test_predict_invalid_input(
        self, client: TestClient, sample_invalid_predict_data: Dict[str, Any]
    ):
        response = client.post("/api/v1/predict", json=sample_invalid_predict_data)
        assert response.status_code == 422

    def test_predict_missing_fields(self, client: TestClient):
        response = client.post("/api/v1/predict", json={})
        assert response.status_code == 422

    def test_predict_with_negative_area(self, client: TestClient):
        data = {
            "Year": 2024,
            "avg_rainfall": 1200.5,
            "pesticides": 45.2,
            "avg_temp": 24.5,
            "area": -100.0,
            "item": "Rice",
        }
        response = client.post("/api/v1/predict", json=data)
        assert response.status_code == 422

    def test_predict_with_year_out_of_range(self, client: TestClient):
        data = {
            "Year": 1900,
            "avg_rainfall": 1200.5,
            "pesticides": 45.2,
            "avg_temp": 24.5,
            "area": 150.0,
            "item": "Rice",
        }
        response = client.post("/api/v1/predict", json=data)
        assert response.status_code == 422

    def test_batch_predict_success(self, client: TestClient):
        payload = [
            {
                "Year": 2024,
                "avg_rainfall": 1200.5,
                "pesticides": 45.2,
                "avg_temp": 24.5,
                "area": 150.0,
                "item": "Rice",
            },
            {
                "Year": 2024,
                "avg_rainfall": 800.0,
                "pesticides": 30.0,
                "avg_temp": 28.0,
                "area": 200.0,
                "item": "Wheat",
            },
        ]
        response = client.post("/api/v1/predict/batch", json=payload)
        assert response.status_code in (200, 201)
        data = response.json()
        assert "predictions" in data
        assert len(data["predictions"]) == 2

    def test_batch_predict_with_invalid_item(self, client: TestClient):
        payload = [
            {
                "Year": 2024,
                "avg_rainfall": 1200.5,
                "pesticides": 45.2,
                "avg_temp": 24.5,
                "area": 150.0,
                "item": "",
            }
        ]
        response = client.post("/api/v1/predict/batch", json=payload)
        assert response.status_code == 422

    def test_prediction_with_mocked_ml(
        self, client: TestClient, sample_predict_data: Dict[str, Any], mocker
    ):
        mock_predict = mocker.patch(
            "app.services.ml_pipeline.MLPipeline.predict",
            return_value={
                "predicted_yield": 5.2,
                "item": "Rice",
                "year": 2024,
                "confidence": 0.87,
            },
        )
        response = client.post("/api/v1/predict", json=sample_predict_data)
        mock_predict.assert_called_once()
        assert response.status_code in (200, 201)
