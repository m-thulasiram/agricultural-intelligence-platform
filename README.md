# CropAI - Crop Health Forecasting Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent agricultural platform that leverages machine learning to forecast crop health, predict yields, assess disease risks, and provide actionable recommendations for farmers and agricultural stakeholders.

---

## Features

1. **Crop Yield Prediction** - ML-powered yield forecasting based on historical climate data, rainfall, temperature, pesticide usage, and area information
2. **Multi-Year Climate Forecasting** - Generate climate forecasts for 5, 10, 20, or 50-year horizons with custom year selection
3. **Disease Risk Assessment** - Predict pest attack probability, disease outbreak likelihood, and seasonal risk levels for specific crops and regions
4. **Crop Recommendations** - Data-driven crop selection with fertilizer plans, irrigation schedules, water-saving strategies, and pest prevention methods
5. **Climate Analysis** - Analyze drought probability, flood risk, and climate impact scores for informed decision-making
6. **Batch Predictions** - Process multiple yield predictions simultaneously for large-scale analysis
7. **Interactive Dashboard** - Real-time analytics with health indices, risk scores, and trend visualizations
8. **PDF Report Generation** - Professional reports with charts, tables, and branded formatting for forecasts, predictions, and comprehensive analysis
9. **Model Comparison** - Compare forecast models (ARIMA, LSTM, Prophet) to select the best approach
10. **User Authentication** - JWT-based authentication with role-based access control
11. **RESTful API** - Well-documented API with OpenAPI/Swagger and ReDoc interfaces
12. **Responsive Frontend** - Modern React UI with Tailwind CSS, routing, and form validation
13. **Database Persistence** - PostgreSQL with SQLAlchemy ORM for reliable data storage
14. **Docker Deployment** - Containerized architecture for easy deployment and scaling

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0 ORM
- **Authentication**: JWT (python-jose) with bcrypt password hashing
- **ML/AI**: scikit-learn, NumPy, Pandas, Joblib
- **PDF Generation**: ReportLab with matplotlib/seaborn charting
- **Validation**: Pydantic v2 with field validators
- **Testing**: pytest with HTTPX TestClient

### Frontend
- **Framework**: React 18 with React Router v6
- **Styling**: Tailwind CSS with custom design system
- **HTTP Client**: Axios with interceptors
- **Charts**: Recharts for data visualization
- **Forms**: React Hook Form with Zod validation
- **Notifications**: react-toastify

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (frontend serving)
- **ASGI Server**: Uvicorn

## Project Structure

```
crop-health-forecasting/
├── backend/
│   ├── app/
│   │   ├── api/                    # API route handlers
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── crop.py             # Crop data model
│   │   │   ├── database.py         # DB engine & session
│   │   │   ├── prediction.py       # Forecast & health models
│   │   │   ├── recommendation.py   # Recommendation model
│   │   │   ├── user.py             # User model
│   │   │   └── weather.py          # Weather data model
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   ├── services/               # Business logic & ML services
│   │   ├── utils/                  # Helpers & PDF report generator
│   │   ├── config.py               # Application settings
│   │   └── main.py                 # FastAPI app entry point
│   ├── tests/                      # Pytest test suite
│   │   ├── conftest.py             # Fixtures & test client
│   │   ├── test_predictions.py     # Yield prediction tests
│   │   ├── test_forecasts.py       # Forecast endpoint tests
│   │   ├── test_diseases.py        # Disease prediction tests
│   │   └── test_recommendations.py # Recommendation tests
│   ├── Dockerfile                  # Backend container build
│   └── requirements.txt            # Python dependencies
├── frontend/
│   ├── public/                     # Static assets & HTML template
│   ├── src/
│   │   ├── components/             # Reusable UI components
│   │   │   ├── charts/             # Chart components (Recharts)
│   │   │   ├── dashboard/          # Dashboard widgets
│   │   │   └── layout/             # Layout & navigation
│   │   ├── pages/                  # Route page components
│   │   ├── services/               # API service modules
│   │   ├── utils/                  # Helpers & Axios client
│   │   ├── __tests__/              # Frontend test suite
│   │   ├── App.js                  # Main app with routing
│   │   └── index.js                # React entry point
│   ├── Dockerfile                  # Multi-stage frontend build
│   ├── package.json                # Node dependencies
│   ├── tailwind.config.js          # Tailwind CSS configuration
│   └── postcss.config.js           # PostCSS configuration
├── docker/
│   └── nginx.conf                  # Nginx configuration
├── models/                         # Trained ML model files
├── reports/                        # Generated PDF reports
├── uploads/                        # File uploads directory
├── docker-compose.yml              # Multi-container setup
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Original Flask project deps
└── README.md                       # This documentation
```

## Prerequisites

- **Docker** & **Docker Compose** (recommended)
- **Python 3.11+** (for manual backend setup)
- **Node.js 18+** & **npm** (for manual frontend setup)
- **PostgreSQL 15** (for manual database setup)

## Quick Start with Docker

The fastest way to run the entire platform:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/crop-health-forecasting.git
cd crop-health-forecasting

# 2. Configure environment (or use defaults)
cp .env.example .env

# 3. Start all services
docker compose up -d

# 4. Verify everything is running
docker compose ps

# 5. Access the application
#    Frontend:  http://localhost:3000
#    API Docs:  http://localhost:8000/api/v1/docs
#    ReDoc:     http://localhost:8000/api/v1/redoc
#    Health:    http://localhost:8000/api/v1/health

# 6. Stop services
docker compose down

# 7. Stop and remove volumes (clean database)
docker compose down -v
```

### Service Ports

| Service   | Port | Description          |
|-----------|------|----------------------|
| Frontend  | 3000 | React web application |
| Backend   | 8000 | FastAPI REST API      |
| PostgreSQL| 5432 | Database              |

## Manual Installation

### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
# Edit backend/.env or set environment variables:
export DATABASE_URL=postgresql://user:password@localhost:5432/crop_health
export SECRET_KEY=your-secret-key-here

# 5. Run database migrations
# Tables are created automatically on first startup

# 6. Start the backend server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

# 7. Verify the API is running
curl http://localhost:8000/api/v1/health
```

### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Configure API URL (optional, defaults to localhost:8000)
# Edit frontend/.env or set:
export REACT_APP_API_URL=http://localhost:8000/api/v1

# 4. Start the development server
npm start

# 5. Open http://localhost:3000 in your browser

# For production build:
npm run build
```

## API Documentation

All API endpoints are prefixed with `/api/v1`. Interactive documentation is available at `/api/v1/docs` (Swagger) and `/api/v1/redoc` (ReDoc).

### Health Check

```
GET /api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Crop Health Forecasting API",
  "version": "1.0.0"
}
```

### Yield Prediction

**Single Prediction**

```
POST /api/v1/predict
```

Request Body:
```json
{
  "Year": 2024,
  "avg_rainfall": 1200.5,
  "pesticides": 45.2,
  "avg_temp": 24.5,
  "area": 150.0,
  "item": "Rice"
}
```

| Field          | Type   | Constraints      | Description               |
|----------------|--------|------------------|---------------------------|
| Year           | int    | 1950-2100        | Year for prediction       |
| avg_rainfall   | float  | >= 0             | Average rainfall (mm)     |
| pesticides     | float  | >= 0             | Pesticide usage (tonnes)  |
| avg_temp       | float  | any              | Average temperature (°C)  |
| area           | float  | >= 0             | Area (hectares)           |
| item           | string | min 1 character  | Crop name                 |

Response:
```json
{
  "predicted_yield": 5.24,
  "item": "Rice",
  "year": 2024,
  "confidence": 0.87
}
```

**Batch Prediction**

```
POST /api/v1/predict/batch
```

Request Body:
```json
{
  "predictions": [
    {
      "Year": 2024,
      "avg_rainfall": 1200.5,
      "pesticides": 45.2,
      "avg_temp": 24.5,
      "area": 150.0,
      "item": "Rice"
    },
    {
      "Year": 2024,
      "avg_rainfall": 800.0,
      "pesticides": 30.0,
      "avg_temp": 28.0,
      "area": 200.0,
      "item": "Wheat"
    }
  ]
}
```

### Climate Forecasting

**Generate Forecast**

```
POST /api/v1/forecast
```

Request Body:
```json
{
  "region": "Punjab",
  "forecast_years": "5"
}
```

| Field          | Type         | Description                                    |
|----------------|--------------|------------------------------------------------|
| region         | string       | Region name (e.g., "Punjab", "Maharashtra")    |
| forecast_years | string       | Preset: "5", "10", "20", "50", or "custom"     |
| custom_years   | list[int]    | Required if forecast_years is "custom"         |

Response:
```json
{
  "region": "Punjab",
  "forecasts": [
    {
      "year": 2025,
      "predicted_yield": 5.4,
      "rainfall_predicted": 1150.0,
      "temperature_predicted": 25.2,
      "confidence": 0.85
    }
  ]
}
```

**Compare Models**

```
POST /api/v1/forecast/compare-models
```

Request Body:
```json
{
  "region": "Punjab",
  "models": ["arima", "lstm", "prophet"],
  "forecast_years": 5
}
```

### Climate Forecast

```
POST /api/v1/climate/forecast
```

Request Body:
```json
{
  "region": "Punjab",
  "year": 2025
}
```

Response:
```json
{
  "id": 1,
  "region": "Punjab",
  "forecast_year": 2025,
  "rainfall_predicted": 1150.5,
  "temperature_predicted": 25.2,
  "drought_probability": 0.15,
  "flood_probability": 0.25,
  "climate_impact_score": 0.45,
  "model_used": "ensemble",
  "confidence_score": 0.85,
  "created_at": "2025-01-15T10:30:00Z"
}
```

### Disease Risk Assessment

```
POST /api/v1/disease/predict
```

Request Body:
```json
{
  "region": "Punjab",
  "crop_type": "Rice",
  "year": 2025
}
```

| Field    | Type   | Constraints | Description      |
|----------|--------|-------------|------------------|
| region   | string | min 1 char  | Region name      |
| crop_type| string | min 1 char  | Crop type        |
| year     | int    | 2024-2100   | Target year      |

Response:
```json
{
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
    "Crop rotation with legumes"
  ]
}
```

**Batch Disease Prediction**

```
POST /api/v1/disease/predict/batch
```

### Crop Recommendations

```
POST /api/v1/recommendations
```

Request Body:
```json
{
  "region": "Punjab",
  "year": 2025,
  "climate_data": {
    "avg_temperature": 26.0,
    "avg_rainfall": 900.0,
    "humidity": 65.0
  }
}
```

Response:
```json
{
  "region": "Punjab",
  "year": 2025,
  "recommended_crops": [
    {
      "name": "Wheat",
      "expected_yield": 4.5,
      "confidence": 0.92,
      "variety": "HD-2967"
    },
    {
      "name": "Rice",
      "expected_yield": 5.2,
      "confidence": 0.88,
      "variety": "Pusa-44"
    }
  ],
  "fertilizer_plan": {
    "nitrogen": 120,
    "phosphorus": 60,
    "potassium": 40,
    "schedule": "Apply NPK 15-15-15 at sowing, top dress urea at 30-35 DAS"
  },
  "irrigation_schedule": {
    "frequency_days": 7,
    "amount_per_session": 50,
    "total_requirement": 450,
    "method": "Drip irrigation recommended"
  },
  "water_saving_strategies": [
    "Mulching to reduce evaporation",
    "Rainwater harvesting",
    "Use of moisture sensors"
  ],
  "pest_prevention_methods": [
    "Integrated pest management",
    "Neem oil spray bi-weekly",
    "Trap crops around field perimeter"
  ]
}
```

### Analytics & Dashboard

```
GET /api/v1/analytics/dashboard
```

Response:
```json
{
  "total_predictions": 1250,
  "average_health_index": 72.5,
  "high_risk_regions": ["Rajasthan", "Gujarat"],
  "climate_trends": {
    "temperature": "increasing",
    "rainfall": "decreasing",
    "drought_risk": "elevated"
  },
  "crop_distribution": {
    "Rice": 450,
    "Wheat": 380,
    "Corn": 210,
    "Sugarcane": 120,
    "Cotton": 90
  }
}
```

```
GET /api/v1/dashboard/summary
```

### History Endpoints

```
GET /api/v1/predictions/history
GET /api/v1/forecasts/history
GET /api/v1/forecasts/region/{region}
GET /api/v1/disease/history
GET /api/v1/disease/summary/{region}
GET /api/v1/recommendations/history
GET /api/v1/predictions/{id}
```

## Machine Learning Model Training

### Training Pipeline

The platform uses ensemble machine learning models for predictions. To train or retrain models:

```bash
# 1. Navigate to the backend
cd backend

# 2. Run the training script (create this script as needed)
python scripts/train_models.py

# 3. Trained models are saved to the models/ directory
#    - yield_prediction_model.pkl
#    - disease_risk_model.pkl
#    - climate_forecast_model.pkl
```

### Sample Training Script

```python
# scripts/train_models.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Load your dataset
data = pd.read_csv("data/crop_yield_data.csv")

# Feature engineering
features = ["Year", "avg_rainfall", "pesticides", "avg_temp", "area"]
X = data[features]
y = data["yield"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
score = model.score(X_test_scaled, y_test)
print(f"Model R² Score: {score:.4f}")

# Save model and scaler
joblib.dump(model, "../models/yield_prediction_model.pkl")
joblib.dump(scaler, "../models/scaler.pkl")
```

### Supported Crop Items

The model supports the following crop types: Rice, Wheat, Maize/Corn, Soybean, Sugarcane, Cotton, Potato, Tomato, Onion, Groundnut, Jute, Tea, Coffee, Coconut, Oil Palm, Fruits (various), Vegetables (various).

### Region Support

Supported regions include: Punjab, Haryana, Uttar Pradesh, Maharashtra, Gujarat, Rajasthan, Madhya Pradesh, Tamil Nadu, Karnataka, Andhra Pradesh, West Bengal, Bihar, Odisha, Assam, Kerala.

## Sample Data

Sample datasets are located in the `datasets/` directory:

- `yield_df.csv` - Historical crop yield data with rainfall, temperature, pesticide usage, and area information

To load sample data:

```python
import pandas as pd

# Load the sample dataset
df = pd.read_csv("datasets/yield_df.csv")
print(df.head())
print(df.columns.tolist())
```

Expected columns: `Year`, `avg_rainfall`, `pesticides`, `avg_temp`, `area`, `item`, `yield`

## Testing

### Backend Tests

The backend test suite uses pytest with FastAPI TestClient.

```bash
# Navigate to project root
cd backend

# Run all tests
pytest tests/ -v

# Run specific test files
pytest tests/test_predictions.py -v
pytest tests/test_forecasts.py -v
pytest tests/test_diseases.py -v
pytest tests/test_recommendations.py -v

# Run with coverage report
pytest tests/ --cov=backend.app --cov-report=term-missing -v

# Run specific test
pytest tests/test_predictions.py::TestPredictionEndpoints::test_health_endpoint -v
```

### Frontend Tests

The frontend test suite uses React Testing Library.

```bash
# Navigate to frontend directory
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watchAll
```

### Test Database

Tests use a SQLite in-memory database (or file-based `test_crop_yield.db`) to avoid affecting the development database. The test database is created fresh for each test session and destroyed after completion.

## Deployment Guide

### Docker Deployment (Production)

```bash
# Build and start services
docker compose -f docker-compose.yml up -d --build

# Scale backend workers
docker compose up -d --scale backend=3

# View logs
docker compose logs -f

# Monitor resource usage
docker stats
```

### Production Checklist

1. **Environment Variables**: Set strong `SECRET_KEY`, database credentials, and CORS origins
2. **Database**: Use managed PostgreSQL (AWS RDS, Azure Database, or Google Cloud SQL)
3. **SSL/TLS**: Configure HTTPS via reverse proxy (Nginx, Traefik, or Cloudflare)
4. **Backup**: Set up automated database backups
5. **Monitoring**: Configure logging, metrics, and alerting
6. **Secrets Management**: Use Docker secrets or a vault service for sensitive data
7. **CI/CD**: Implement continuous integration and deployment pipeline

### Manual Deployment

```bash
# Backend (using systemd or supervisor)
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend (serve with Nginx)
npm run build
cp -r build/* /var/www/html/

# Nginx configuration (see docker/nginx.conf)
```

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository** and create your feature branch
2. **Write tests** for any new functionality
3. **Ensure all tests pass** before submitting
4. **Follow the existing code style** (linting, formatting)
5. **Submit a pull request** with a clear description of changes

### Development Workflow

```bash
# Create a feature branch
git checkout -b feature/amazing-feature

# Make changes and test
pytest tests/ -v

# Commit with conventional commit format
git commit -m "feat: add amazing new feature"

# Push and create PR
git push origin feature/amazing-feature
```

### Code Style

- Python: Follow PEP 8, use type hints
- JavaScript: Follow ESLint configuration
- Git: Use conventional commit format (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ for sustainable agriculture and food security.
