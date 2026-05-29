import logging
from datetime import datetime

from .models.database import SessionLocal, init_db
from .models.user import User
from .models.crop import Crop
from .models.weather import WeatherData
from .models.prediction import ClimateForecast, CropHealthPrediction, DiseasePrediction
from .models.recommendation import Recommendation

logger = logging.getLogger(__name__)


def seed_database():
    init_db()
    db = SessionLocal()
    try:
        if db.query(User).first():
            logger.info("Database already seeded, skipping.")
            return

        admin = User(
            username="admin",
            email="admin@cropai.com",
            hashed_password="$2b$12$dummy_hash_for_admin",
            is_active=True,
            is_admin=True,
        )
        db.add(admin)

        crops_data = [
            {"name": "Rice", "type": "cereal", "region": "North India", "soil_type": "alluvial", "water_requirement": 1200.0, "temperature_min": 20.0, "temperature_max": 38.0, "growing_season": "kharif"},
            {"name": "Wheat", "type": "cereal", "region": "North India", "soil_type": "loamy", "water_requirement": 450.0, "temperature_min": 10.0, "temperature_max": 25.0, "growing_season": "rabi"},
            {"name": "Maize", "type": "cereal", "region": "Central India", "soil_type": "loamy", "water_requirement": 600.0, "temperature_min": 18.0, "temperature_max": 35.0, "growing_season": "kharif"},
            {"name": "Cotton", "type": "fiber", "region": "West India", "soil_type": "black", "water_requirement": 700.0, "temperature_min": 20.0, "temperature_max": 37.0, "growing_season": "kharif"},
            {"name": "Sugarcane", "type": "cash", "region": "South India", "soil_type": "loamy", "water_requirement": 1500.0, "temperature_min": 20.0, "temperature_max": 38.0, "growing_season": "annual"},
            {"name": "Potato", "type": "vegetable", "region": "North India", "soil_type": "sandy_loam", "water_requirement": 500.0, "temperature_min": 12.0, "temperature_max": 25.0, "growing_season": "rabi"},
            {"name": "Soybean", "type": "oilseed", "region": "Central India", "soil_type": "loamy", "water_requirement": 500.0, "temperature_min": 18.0, "temperature_max": 32.0, "growing_season": "kharif"},
        ]
        for c in crops_data:
            db.add(Crop(**c))

        regions = ["North India", "South India", "East India", "West India", "Central India"]
        for region in regions:
            for year in range(2020, 2026):
                wd = WeatherData(
                    region=region,
                    year=year,
                    rainfall=800.0 + hash(f"{region}_{year}") % 600,
                    temperature=22.0 + hash(f"{region}_temp_{year}") % 10,
                    humidity=60.0 + hash(f"{region}_hum_{year}") % 30,
                    soil_ph=6.5 + hash(f"{region}_ph_{year}") % 10 * 0.1,
                    soil_moisture=30.0 + hash(f"{region}_sm_{year}") % 40,
                    nitrogen=80.0 + hash(f"{region}_n_{year}") % 60,
                    phosphorus=30.0 + hash(f"{region}_p_{year}") % 30,
                    potassium=40.0 + hash(f"{region}_k_{year}") % 40,
                )
                db.add(wd)

        for region in regions:
            for year in [2025, 2026, 2027]:
                cf = ClimateForecast(
                    region=region,
                    forecast_year=year,
                    rainfall_predicted=850.0 + hash(f"{region}_rf_{year}") % 400,
                    temperature_predicted=24.0 + hash(f"{region}_tp_{year}") % 6,
                    drought_probability=abs(hash(f"{region}_dr_{year}") % 100) / 100.0,
                    flood_probability=abs(hash(f"{region}_fl_{year}") % 100) / 100.0,
                    climate_impact_score=60.0 + abs(hash(f"{region}_ci_{year}") % 40),
                    model_used="ClimateEnsemble",
                    confidence_score=0.75 + abs(hash(f"{region}_cs_{year}") % 20) / 100.0,
                )
                db.add(cf)

        db.commit()
        logger.info("Database seeded successfully with sample data.")

    except Exception as e:
        db.rollback()
        logger.error("Seeding failed: %s", str(e))
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_database()
