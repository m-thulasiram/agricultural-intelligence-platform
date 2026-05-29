import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any


class TestForecastEndpoints:
    def test_forecast_with_valid_data(
        self, client: TestClient, sample_forecast_data: Dict[str, Any]
    ):
        response = client.post("/api/v1/forecast/future", json=sample_forecast_data)
        assert response.status_code in (200, 201)
        data = response.json()
        assert "region" in data
        assert data["region"] == sample_forecast_data["region"]
        assert "forecasts" in data

    def test_forecast_with_custom_years(self, client: TestClient):
        data = {
            "region": "Punjab",
            "forecast_years": "custom",
            "custom_years": [2026, 2028, 2030],
        }
        response = client.post("/api/v1/forecast/future", json=data)
        assert response.status_code in (200, 201)
        result = response.json()
        assert result["region"] == "Punjab"

    def test_forecast_with_ten_year_preset(self, client: TestClient):
        data = {"region": "Maharashtra", "forecast_years": "10"}
        response = client.post("/api/v1/forecast/future", json=data)
        assert response.status_code in (200, 201)
        result = response.json()
        assert result["region"] == "Maharashtra"

    def test_forecast_with_twenty_year_preset(self, client: TestClient):
        data = {"region": "Gujarat", "forecast_years": "20"}
        response = client.post("/api/v1/forecast/future", json=data)
        assert response.status_code in (200, 201)
        result = response.json()
        assert result["region"] == "Gujarat"

    def test_forecast_with_invalid_preset(self, client: TestClient):
        data = {"region": "Punjab", "forecast_years": "invalid"}
        response = client.post("/api/v1/forecast/future", json=data)
        assert response.status_code == 422

    def test_forecast_with_empty_region(self, client: TestClient):
        data = {"region": "", "forecast_years": "5"}
        response = client.post("/api/v1/forecast/future", json=data)
        assert response.status_code == 422

    def test_compare_models(self, client: TestClient):
        data = {
            "region": "Punjab",
            "forecast_years": 5,
        }
        response = client.post("/api/v1/forecast/compare-models", json=data)
        assert response.status_code in (200, 201)

    def test_compare_models_default(
        self, client: TestClient, sample_forecast_data: Dict[str, Any]
    ):
        data = {"region": "Punjab", "forecast_years": 5}
        response = client.post("/api/v1/forecast/compare-models", json=data)
        assert response.status_code in (200, 201)

    def test_get_forecast_history(self, client: TestClient):
        response = client.get("/api/v1/forecast/history/Punjab")
        assert response.status_code in (200, 404)

    def test_forecast_service_error_handling(
        self, client: TestClient, sample_forecast_data: Dict[str, Any], mocker
    ):
        mocker.patch(
            "app.services.forecasting.ClimateForecaster.forecast_future",
            side_effect=Exception("Model training failed"),
        )
        response = client.post("/api/v1/forecast/future", json=sample_forecast_data)
        assert response.status_code in (500, 503)

    def test_dynamic_timeline_with_future_years(self, client: TestClient):
        data = {"region": "Punjab", "start_year": 2025, "n": 5}
        response = client.post("/api/v1/forecast/timeline", json=data)
        assert response.status_code in (200, 201)
        result = response.json()
        assert result["region"] == "Punjab"
        assert result["start_year"] == 2025
        assert result["end_year"] == 2030
        assert result["total_years"] == 6
        assert len(result["timeline"]) == 6
        assert result["timeline"][0]["year"] == 2025
        assert result["timeline"][5]["year"] == 2030
        for entry in result["timeline"]:
            assert "rainfall" in entry
            assert "temperature" in entry
            assert "humidity" in entry
            assert "fertilizer_usage" in entry
            assert "pesticide_usage" in entry
            assert "crop_yield" in entry
            assert "crop_health_index" in entry
            assert "disease_risk" in entry
            assert "pest_risk" in entry
            assert "water_stress" in entry
            assert "sustainability_score" in entry

    def test_dynamic_timeline_with_historical_years(self, client: TestClient):
        data = {"region": "Gujarat", "start_year": 2010, "n": 10}
        response = client.post("/api/v1/forecast/timeline", json=data)
        assert response.status_code in (200, 201)
        result = response.json()
        assert result["start_year"] == 2010
        assert result["end_year"] == 2020
        assert result["total_years"] == 11

    def test_dynamic_timeline_with_large_n(self, client: TestClient):
        data = {"region": "Maharashtra", "start_year": 2000, "n": 50}
        response = client.post("/api/v1/forecast/timeline", json=data)
        assert response.status_code in (200, 201)
        result = response.json()
        assert result["start_year"] == 2000
        assert result["end_year"] == 2050
        assert result["total_years"] == 51

    def test_dynamic_timeline_with_zero_n(self, client: TestClient):
        data = {"region": "Punjab", "start_year": 2025, "n": 0}
        response = client.post("/api/v1/forecast/timeline", json=data)
        assert response.status_code in (200, 201)
        result = response.json()
        assert result["start_year"] == 2025
        assert result["end_year"] == 2025
        assert result["total_years"] == 1
        assert len(result["timeline"]) == 1

    def test_dynamic_timeline_with_empty_region(self, client: TestClient):
        data = {"region": "", "start_year": 2025, "n": 5}
        response = client.post("/api/v1/forecast/timeline", json=data)
        assert response.status_code == 422

    def test_dynamic_timeline_service_error(
        self, client: TestClient, mocker
    ):
        mocker.patch(
            "app.services.forecasting.ClimateForecaster.generate_dynamic_timeline",
            side_effect=Exception("Generation failed"),
        )
        data = {"region": "Punjab", "start_year": 2025, "n": 5}
        response = client.post("/api/v1/forecast/timeline", json=data)
        assert response.status_code in (500, 503)
