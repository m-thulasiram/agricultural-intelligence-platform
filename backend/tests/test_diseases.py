import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any


class TestDiseasePredictionEndpoints:
    def test_disease_prediction_valid(
        self, client: TestClient, sample_disease_data: Dict[str, Any]
    ):
        response = client.post("/api/v1/disease/risk", json=sample_disease_data)
        assert response.status_code in (200, 201)
        data = response.json()
        assert "region" in data
        assert "crop_type" in data
        assert "year" in data
        assert "pest_attack_probability" in data
        assert "disease_outbreak_probability" in data
        assert "seasonal_risk" in data
        assert "preventive_measures" in data

    def test_disease_prediction_invalid_crop(self, client: TestClient):
        data = {"region": "Punjab", "crop_type": "", "year": 2025}
        response = client.post("/api/v1/disease/risk", json=data)
        assert response.status_code == 422

    def test_disease_prediction_invalid_year(self, client: TestClient):
        data = {"region": "Punjab", "crop_type": "Rice", "year": 2000}
        response = client.post("/api/v1/disease/risk", json=data)
        assert response.status_code == 422

    def test_disease_prediction_year_in_future(self, client: TestClient):
        data = {"region": "Punjab", "crop_type": "Wheat", "year": 2101}
        response = client.post("/api/v1/disease/risk", json=data)
        assert response.status_code == 422

    def test_disease_prediction_empty_region(self, client: TestClient):
        data = {"region": "", "crop_type": "Rice", "year": 2025}
        response = client.post("/api/v1/disease/risk", json=data)
        assert response.status_code == 422

    def test_disease_risk_probability_range(
        self, client: TestClient, sample_disease_data: Dict[str, Any]
    ):
        response = client.post("/api/v1/disease/risk", json=sample_disease_data)
        assert response.status_code in (200, 201)
        data = response.json()
        assert 0.0 <= data["pest_attack_probability"] <= 1.0
        assert 0.0 <= data["disease_outbreak_probability"] <= 1.0

    def test_disease_seasonal_risk_valid(
        self, client: TestClient, sample_disease_data: Dict[str, Any]
    ):
        response = client.post("/api/v1/disease/risk", json=sample_disease_data)
        assert response.status_code in (200, 201)
        data = response.json()
        valid_risks = {"Low", "Moderate", "High", "Critical"}
        assert data["seasonal_risk"] in valid_risks

    def test_disease_preventive_measures_not_empty(
        self, client: TestClient, sample_disease_data: Dict[str, Any]
    ):
        response = client.post("/api/v1/disease/risk", json=sample_disease_data)
        assert response.status_code in (200, 201)
        data = response.json()
        assert len(data["preventive_measures"]) > 0

    def test_disease_prediction_different_crops(self, client: TestClient):
        crops = ["Rice", "Wheat", "Corn", "Sugarcane", "Cotton"]
        for crop in crops:
            data = {"region": "Punjab", "crop_type": crop, "year": 2025}
            response = client.post("/api/v1/disease/risk", json=data)
            assert response.status_code in (200, 201)

    def test_disease_prediction_different_regions(self, client: TestClient):
        regions = ["Punjab", "Maharashtra", "Gujarat", "Tamil Nadu", "Karnataka"]
        for region in regions:
            data = {"region": region, "crop_type": "Rice", "year": 2025}
            response = client.post("/api/v1/disease/risk", json=data)
            assert response.status_code in (200, 201)

    def test_disease_history_endpoint(self, client: TestClient):
        response = client.get("/api/v1/disease/history/Punjab")
        assert response.status_code in (200, 404)

    def test_disease_prediction_with_mocked_service(
        self, client: TestClient, sample_disease_data: Dict[str, Any], mocker
    ):
        mock_result = {
            "region": "Punjab",
            "crop_type": "Rice",
            "year": 2025,
            "pest_attack_probability": 0.35,
            "disease_outbreak_probability": 0.25,
            "seasonal_risk": "Moderate",
            "preventive_measures": [
                "Apply neem oil bi-weekly",
                "Maintain proper drainage",
                "Use resistant seed varieties",
                "Crop rotation with legumes",
            ],
        }
        mock_predict = mocker.patch(
            "app.services.disease_predictor.DiseasePredictor.predict_risk",
            return_value=mock_result,
        )
        response = client.post("/api/v1/disease/risk", json=sample_disease_data)
        mock_predict.assert_called_once()
        assert response.status_code in (200, 201)
        result = response.json()
        assert result == mock_result

    def test_disease_batch_predict(self, client: TestClient):
        payload = [
            {"region": "Punjab", "crop_type": "Rice", "year": 2025},
            {"region": "Maharashtra", "crop_type": "Wheat", "year": 2026},
        ]
        response = client.post("/api/v1/disease/batch", json=payload)
        assert response.status_code in (200, 201)
