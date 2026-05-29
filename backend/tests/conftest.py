import pytest
from typing import Generator, Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_crop_yield.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def sample_predict_data() -> Dict[str, Any]:
    return {
        "Year": 2024,
        "avg_rainfall": 1200.5,
        "pesticides": 45.2,
        "avg_temp": 24.5,
        "area": 150.0,
        "item": "Rice",
    }


@pytest.fixture()
def sample_invalid_predict_data() -> Dict[str, Any]:
    return {
        "Year": 2024,
        "avg_rainfall": -10.0,
        "pesticides": 45.2,
        "avg_temp": 24.5,
        "area": 150.0,
        "item": "Rice",
    }


@pytest.fixture()
def sample_forecast_data() -> Dict[str, Any]:
    return {
        "region": "Punjab",
        "forecast_years": "5",
    }


@pytest.fixture()
def sample_disease_data() -> Dict[str, Any]:
    return {
        "region": "Punjab",
        "crop_type": "Rice",
        "year": 2025,
    }


@pytest.fixture()
def sample_recommendation_data() -> Dict[str, Any]:
    return {
        "region": "Punjab",
        "year": 2025,
    }
