"""initial migration

Revision ID: 001
Revises:
Create Date: 2026-05-29

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.create_table(
        "crops",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("type", sa.String(length=100), nullable=False),
        sa.Column("region", sa.String(length=150), nullable=False),
        sa.Column("soil_type", sa.String(length=100), nullable=False),
        sa.Column("water_requirement", sa.Float(), nullable=False),
        sa.Column("temperature_min", sa.Float(), nullable=False),
        sa.Column("temperature_max", sa.Float(), nullable=False),
        sa.Column("growing_season", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_crops_id"), "crops", ["id"], unique=False)
    op.create_index(op.f("ix_crops_name"), "crops", ["name"], unique=False)
    op.create_index(op.f("ix_crops_region"), "crops", ["region"], unique=False)

    op.create_table(
        "weather_data",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("region", sa.String(length=150), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("rainfall", sa.Float(), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.Column("humidity", sa.Float(), nullable=False),
        sa.Column("soil_ph", sa.Float(), nullable=False),
        sa.Column("soil_moisture", sa.Float(), nullable=False),
        sa.Column("nitrogen", sa.Float(), nullable=False),
        sa.Column("phosphorus", sa.Float(), nullable=False),
        sa.Column("potassium", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_weather_data_id"), "weather_data", ["id"], unique=False)
    op.create_index(op.f("ix_weather_data_region"), "weather_data", ["region"], unique=False)
    op.create_index(op.f("ix_weather_data_year"), "weather_data", ["year"], unique=False)

    op.create_table(
        "climate_forecasts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("region", sa.String(length=150), nullable=False),
        sa.Column("forecast_year", sa.Integer(), nullable=False),
        sa.Column("rainfall_predicted", sa.Float(), nullable=False),
        sa.Column("temperature_predicted", sa.Float(), nullable=False),
        sa.Column("drought_probability", sa.Float(), nullable=False),
        sa.Column("flood_probability", sa.Float(), nullable=False),
        sa.Column("climate_impact_score", sa.Float(), nullable=False),
        sa.Column("model_used", sa.String(length=150), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_climate_forecasts_id"), "climate_forecasts", ["id"], unique=False)
    op.create_index(op.f("ix_climate_forecasts_region"), "climate_forecasts", ["region"], unique=False)
    op.create_index(op.f("ix_climate_forecasts_forecast_year"), "climate_forecasts", ["forecast_year"], unique=False)

    op.create_table(
        "crop_health_predictions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("region", sa.String(length=150), nullable=False),
        sa.Column("crop_type", sa.String(length=100), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("health_index", sa.Float(), nullable=False),
        sa.Column("yield_forecast", sa.Float(), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("health_category", sa.String(length=50), nullable=False),
        sa.Column("model_used", sa.String(length=150), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_crop_health_predictions_id"), "crop_health_predictions", ["id"], unique=False)
    op.create_index(op.f("ix_crop_health_predictions_region"), "crop_health_predictions", ["region"], unique=False)
    op.create_index(op.f("ix_crop_health_predictions_crop_type"), "crop_health_predictions", ["crop_type"], unique=False)
    op.create_index(op.f("ix_crop_health_predictions_year"), "crop_health_predictions", ["year"], unique=False)

    op.create_table(
        "disease_predictions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("region", sa.String(length=150), nullable=False),
        sa.Column("crop_type", sa.String(length=100), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("pest_attack_probability", sa.Float(), nullable=False),
        sa.Column("disease_outbreak_probability", sa.Float(), nullable=False),
        sa.Column("seasonal_risk", sa.String(length=50), nullable=False),
        sa.Column("preventive_measures", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_disease_predictions_id"), "disease_predictions", ["id"], unique=False)
    op.create_index(op.f("ix_disease_predictions_region"), "disease_predictions", ["region"], unique=False)
    op.create_index(op.f("ix_disease_predictions_crop_type"), "disease_predictions", ["crop_type"], unique=False)
    op.create_index(op.f("ix_disease_predictions_year"), "disease_predictions", ["year"], unique=False)

    op.create_table(
        "recommendations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("region", sa.String(length=150), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("recommended_crops", sa.JSON(), nullable=False),
        sa.Column("fertilizer_plan", sa.JSON(), nullable=False),
        sa.Column("irrigation_schedule", sa.JSON(), nullable=False),
        sa.Column("water_saving_strategies", sa.JSON(), nullable=False),
        sa.Column("pest_prevention_methods", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_recommendations_id"), "recommendations", ["id"], unique=False)
    op.create_index(op.f("ix_recommendations_region"), "recommendations", ["region"], unique=False)
    op.create_index(op.f("ix_recommendations_year"), "recommendations", ["year"], unique=False)


def downgrade() -> None:
    op.drop_table("recommendations")
    op.drop_table("disease_predictions")
    op.drop_table("crop_health_predictions")
    op.drop_table("climate_forecasts")
    op.drop_table("weather_data")
    op.drop_table("crops")
    op.drop_table("users")
