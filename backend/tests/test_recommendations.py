import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any


class TestRecommendationEndpoints:
    def test_recommendation_valid(
        self, client: TestClient, sample_recommendation_data: Dict[str, Any]
    ):
        response = client.post(
            "/api/v1/recommendation/crop", json=sample_recommendation_data
        )
        assert response.status_code in (200, 201)
        data = response.json()
        assert "region" in data
        assert "year" in data
        assert "recommended_crops" in data
        assert "fertilizer_plan" in data
        assert "irrigation_schedule" in data
        assert "water_saving_strategies" in data
        assert "pest_prevention_methods" in data

    def test_recommendation_empty_region(self, client: TestClient):
        data = {"region": "", "year": 2025}
        response = client.post("/api/v1/recommendation/crop", json=data)
        assert response.status_code == 422

    def test_recommendation_invalid_year(self, client: TestClient):
        data = {"region": "Punjab", "year": 1900}
        response = client.post("/api/v1/recommendation/crop", json=data)
        assert response.status_code == 422

    def test_recommendation_year_too_far(self, client: TestClient):
        data = {"region": "Punjab", "year": 2200}
        response = client.post("/api/v1/recommendation/crop", json=data)
        assert response.status_code == 422

    def test_recommendation_with_climate_override(
        self, client: TestClient, sample_recommendation_data: Dict[str, Any]
    ):
        data = {
            **sample_recommendation_data,
            "climate_data": {
                "avg_temperature": 26.0,
                "avg_rainfall": 900.0,
                "humidity": 65.0,
            },
        }
        response = client.post("/api/v1/recommendation/crop", json=data)
        assert response.status_code in (200, 201)

    def test_recommended_crops_structured(
        self, client: TestClient, sample_recommendation_data: Dict[str, Any]
    ):
        response = client.post(
            "/api/v1/recommendation/crop", json=sample_recommendation_data
        )
        assert response.status_code in (200, 201)
        data = response.json()
        for crop in data["recommended_crops"]:
            assert "crop_name" in crop or "name" in crop

    def test_recommendation_different_regions(self, client: TestClient):
        regions = ["Punjab", "Rajasthan", "Kerala", "Uttar Pradesh", "West Bengal"]
        for region in regions:
            data = {"region": region, "year": 2025}
            response = client.post("/api/v1/recommendation/crop", json=data)
            assert response.status_code in (200, 201)

    def test_recommendation_with_mocked_service(
        self, client: TestClient, sample_recommendation_data: Dict[str, Any], mocker
    ):
        mock_result = {
            "region": "Punjab",
            "year": 2025,
            "recommended_crops": [
                {
                    "crop_name": "Wheat",
                    "suitability_score": 0.92,
                },
                {
                    "crop_name": "Rice",
                    "suitability_score": 0.88,
                },
            ],
            "fertilizer_plan": {},
            "irrigation_schedule": {},
            "water_saving_strategies": [
                "Mulching to reduce evaporation",
                "Rainwater harvesting",
            ],
            "pest_prevention_methods": [
                "Integrated pest management",
                "Neem oil spray bi-weekly",
            ],
        }
        mock_rec = mocker.patch(
            "app.services.recommendation_engine.RecommendationEngine.recommend_crops",
            return_value=mock_result,
        )
        response = client.post(
            "/api/v1/recommendation/crop", json=sample_recommendation_data
        )
        mock_rec.assert_called_once()
        assert response.status_code in (200, 201)
        result = response.json()
        assert result == mock_result

    def test_analytics_dashboard_summary(self, client: TestClient):
        response = client.get("/api/v1/analytics/dashboard-summary")
        assert response.status_code in (200, 201)
