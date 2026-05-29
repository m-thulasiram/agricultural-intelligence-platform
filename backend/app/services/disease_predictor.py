from typing import Any, Dict, List, Optional
from datetime import datetime

import numpy as np


class DiseasePredictor:
    def __init__(self):
        self.crop_pest_profiles = {
            "maize": {
                "pests": ["fall_armyworm", "stem_borer", "maize_weevil"],
                "optimal_temp": (20, 30),
                "optimal_rainfall": (500, 1200),
                "humidity_threshold": 70,
            },
            "wheat": {
                "pests": ["aphid", "wheat_stem_rust", "powdery_mildew"],
                "optimal_temp": (15, 25),
                "optimal_rainfall": (400, 900),
                "humidity_threshold": 65,
            },
            "rice": {
                "pests": ["brown_planthopper", "stem_borer", "rice_blast"],
                "optimal_temp": (22, 32),
                "optimal_rainfall": (1000, 2000),
                "humidity_threshold": 75,
            },
            "potato": {
                "pests": ["colorado_beetle", "late_blight", "early_blight"],
                "optimal_temp": (15, 22),
                "optimal_rainfall": (500, 1000),
                "humidity_threshold": 70,
            },
            "soybean": {
                "pests": ["soybean_aphid", "rust", "root_rot"],
                "optimal_temp": (20, 30),
                "optimal_rainfall": (600, 1200),
                "humidity_threshold": 65,
            },
            "sorghum": {
                "pests": ["sorghum_midge", "stem_borer", "head_smut"],
                "optimal_temp": (22, 32),
                "optimal_rainfall": (400, 800),
                "humidity_threshold": 60,
            },
        }

        self.crop_disease_profiles = {
            "maize": {
                "diseases": ["northern_leaf_blight", "gray_leaf_spot", "common_rust"],
                "temp_range": (18, 28),
                "humidity_threshold": 75,
                "rainfall_risk": 800,
            },
            "wheat": {
                "diseases": ["stripe_rust", "leaf_rust", "fusarium_head_blight"],
                "temp_range": (15, 25),
                "humidity_threshold": 70,
                "rainfall_risk": 600,
            },
            "rice": {
                "diseases": ["rice_blast", "sheath_blight", "bacterial_blight"],
                "temp_range": (22, 32),
                "humidity_threshold": 80,
                "rainfall_risk": 1200,
            },
            "potato": {
                "diseases": ["late_blight", "early_blight", "black_scurf"],
                "temp_range": (15, 22),
                "humidity_threshold": 75,
                "rainfall_risk": 700,
            },
            "soybean": {
                "diseases": ["soybean_rust", "downy_mildew", "brown_spot"],
                "temp_range": (20, 28),
                "humidity_threshold": 70,
                "rainfall_risk": 800,
            },
        }

        self.seasonal_risk_patterns = {
            "spring": {
                "base_risk": 0.3,
                "temperature_amplification": 0.02,
                "rainfall_amplification": 0.015,
            },
            "summer": {
                "base_risk": 0.5,
                "temperature_amplification": 0.04,
                "rainfall_amplification": 0.03,
            },
            "monsoon": {
                "base_risk": 0.7,
                "temperature_amplification": 0.03,
                "rainfall_amplification": 0.05,
            },
            "autumn": {
                "base_risk": 0.4,
                "temperature_amplification": 0.02,
                "rainfall_amplification": 0.02,
            },
            "winter": {
                "base_risk": 0.2,
                "temperature_amplification": 0.01,
                "rainfall_amplification": 0.01,
            },
            "dry": {
                "base_risk": 0.25,
                "temperature_amplification": 0.03,
                "rainfall_amplification": 0.005,
            },
        }

        self.region_risk_modifiers = {
            "tropical": 1.3,
            "subtropical": 1.15,
            "temperate": 0.85,
            "arid": 0.7,
            "mediterranean": 0.9,
            "continental": 0.8,
        }

    def _get_climate_deviation_factor(
        self, climate_data: Dict[str, float], crop_type: str
    ) -> float:
        crop_lower = crop_type.lower()
        profile = self.crop_pest_profiles.get(
            crop_lower,
            {"optimal_temp": (15, 30), "optimal_rainfall": (400, 1200), "humidity_threshold": 65},
        )

        temp = climate_data.get("temperature", 25)
        rainfall = climate_data.get("rainfall", 800)
        humidity = climate_data.get("humidity", 60)

        temp_min, temp_max = profile["optimal_temp"]
        temp_deviation = 0
        if temp < temp_min:
            temp_deviation = (temp_min - temp) / temp_min
        elif temp > temp_max:
            temp_deviation = (temp - temp_max) / temp_max

        rain_min, rain_max = profile["optimal_rainfall"]
        rain_deviation = 0
        if rainfall < rain_min:
            rain_deviation = (rain_min - rainfall) / rain_min
        elif rainfall > rain_max:
            rain_deviation = (rainfall - rain_max) / rain_max

        hum_deviation = max(0, (humidity - profile["humidity_threshold"]) / (100 - profile["humidity_threshold"]))

        deviation_factor = 0.4 * temp_deviation + 0.35 * rain_deviation + 0.25 * hum_deviation
        return min(1.0, max(0.0, deviation_factor))

    def _get_region_modifier(self, region: str) -> float:
        region_lower = region.lower()
        for key, modifier in self.region_risk_modifiers.items():
            if key in region_lower:
                return modifier
        return 1.0

    def predict_pest_attack(
        self, region: str, crop_type: str, climate_data: Dict[str, float]
    ) -> float:
        deviation = self._get_climate_deviation_factor(climate_data, crop_type)
        region_mod = self._get_region_modifier(region)

        historical_base = 0.15
        np.random.seed(hash(f"{region}_{crop_type}") % (2**31))

        pest_probability = historical_base + 0.6 * deviation + 0.05 * region_mod + np.random.uniform(-0.05, 0.05)
        pest_probability = min(1.0, max(0.0, pest_probability))

        return round(float(pest_probability), 4)

    def predict_disease_outbreak(
        self, region: str, crop_type: str, climate_data: Dict[str, float]
    ) -> float:
        deviation = self._get_climate_deviation_factor(climate_data, crop_type)
        region_mod = self._get_region_modifier(region)
        crop_lower = crop_type.lower()

        disease_profile = self.crop_disease_profiles.get(
            crop_lower,
            {"temp_range": (15, 30), "humidity_threshold": 65, "rainfall_risk": 800},
        )

        temp = climate_data.get("temperature", 25)
        rainfall = climate_data.get("rainfall", 800)
        humidity = climate_data.get("humidity", 60)

        temp_min, temp_max = disease_profile["temp_range"]
        temp_in_range = 1.0 if temp_min <= temp <= temp_max else 0.5

        rain_factor = min(1.0, rainfall / disease_profile["rainfall_risk"])
        hum_factor = min(1.0, humidity / disease_profile["humidity_threshold"])

        disease_risk = 0.3 * deviation + 0.3 * (1 - temp_in_range) + 0.2 * rain_factor + 0.2 * hum_factor
        disease_risk *= region_mod

        np.random.seed(hash(f"{region}_{crop_type}_disease") % (2**31))
        disease_risk += np.random.uniform(-0.05, 0.05)
        disease_risk = min(1.0, max(0.0, disease_risk))

        return round(float(disease_risk), 4)

    def assess_seasonal_risk(self, region: str, season: str) -> Dict[str, Any]:
        season_lower = season.lower().strip()
        region_mod = self._get_region_modifier(region)

        pattern = self.seasonal_risk_patterns.get(
            season_lower,
            {"base_risk": 0.4, "temperature_amplification": 0.02, "rainfall_amplification": 0.02},
        )

        base_risk = pattern["base_risk"] * region_mod

        temp_amplification = pattern["temperature_amplification"]
        rain_amplification = pattern["rainfall_amplification"]

        risk_score = min(1.0, base_risk + temp_amplification + rain_amplification)

        if risk_score < 0.2:
            risk_level = "Very Low"
        elif risk_score < 0.35:
            risk_level = "Low"
        elif risk_score < 0.5:
            risk_level = "Moderate"
        elif risk_score < 0.7:
            risk_level = "High"
        else:
            risk_level = "Very High"

        common_pests = {
            "spring": ["aphids", "cutworms"],
            "summer": ["whiteflies", "thrips"],
            "monsoon": ["snails", "fungal vectors"],
            "autumn": ["caterpillars", "mites"],
            "winter": ["fungal pathogens", "rodents"],
            "dry": ["spider_mites", "thrips"],
        }
        expected_pests = common_pests.get(season_lower, ["general_pests"])

        return {
            "season": season,
            "region": region,
            "risk_score": round(risk_score, 4),
            "risk_level": risk_level,
            "expected_pests": expected_pests,
            "recommended_monitoring": (
                "weekly" if risk_score > 0.5 else "biweekly"
            ),
        }

    def get_preventive_measures(
        self, disease_type: str, crop_type: str
    ) -> List[Dict[str, str]]:
        measures = []

        general_measures = [
            {
                "category": "Cultural Control",
                "measure": "Crop rotation with non-host crops for at least 2 seasons",
                "priority": "High",
            },
            {
                "category": "Cultural Control",
                "measure": "Use certified disease-free seeds and planting material",
                "priority": "High",
            },
            {
                "category": "Sanitation",
                "measure": "Remove and destroy infected plant debris after harvest",
                "priority": "Medium",
            },
        ]

        disease_specific = {
            "blight": [
                {
                    "category": "Chemical Control",
                    "measure": "Apply copper-based fungicides at first sign of infection",
                    "priority": "High",
                },
                {
                    "category": "Cultural Control",
                    "measure": "Ensure proper plant spacing for air circulation",
                    "priority": "Medium",
                },
                {
                    "category": "Resistant Varieties",
                    "measure": "Plant blight-resistant varieties when available",
                    "priority": "High",
                },
            ],
            "rust": [
                {
                    "category": "Chemical Control",
                    "measure": "Apply sulfur or triazole fungicides preventively",
                    "priority": "High",
                },
                {
                    "category": "Cultural Control",
                    "measure": "Avoid overhead irrigation to reduce leaf wetness",
                    "priority": "Medium",
                },
                {
                    "category": "Biological Control",
                    "measure": "Introduce biocontrol agents like Bacillus subtilis",
                    "priority": "Low",
                },
            ],
            "mildew": [
                {
                    "category": "Chemical Control",
                    "measure": "Apply potassium bicarbonate or neem oil spray",
                    "priority": "Medium",
                },
                {
                    "category": "Cultural Control",
                    "measure": "Reduce nitrogen fertilization to decrease susceptibility",
                    "priority": "Medium",
                },
            ],
            "borer": [
                {
                    "category": "Biological Control",
                    "measure": "Release Trichogramma egg parasitoids",
                    "priority": "High",
                },
                {
                    "category": "Chemical Control",
                    "measure": "Apply systemic insecticides at early stage",
                    "priority": "Medium",
                },
            ],
            "aphid": [
                {
                    "category": "Biological Control",
                    "measure": "Encourage beneficial insects like ladybugs and lacewings",
                    "priority": "High",
                },
                {
                    "category": "Chemical Control",
                    "measure": "Apply insecticidal soap or neem oil for severe infestations",
                    "priority": "Low",
                },
            ],
            "weevil": [
                {
                    "category": "Cultural Control",
                    "measure": "Store harvested grains in airtight containers with neem leaves",
                    "priority": "High",
                },
                {
                    "category": "Chemical Control",
                    "measure": "Fumigate storage areas before grain storage",
                    "priority": "Medium",
                },
            ],
            "moth": [
                {
                    "category": "Biological Control",
                    "measure": "Use pheromone traps to monitor and control populations",
                    "priority": "Medium",
                },
                {
                    "category": "Cultural Control",
                    "measure": "Deep plowing after harvest to expose pupae",
                    "priority": "Medium",
                },
            ],
        }

        measures.extend(general_measures)

        disease_lower = disease_type.lower()
        for key, specific in disease_specific.items():
            if key in disease_lower:
                measures.extend(specific)

        crop_specific_hints = {
            "maize": "Practice stem borer control through intercropping with legumes",
            "wheat": "Ensure balanced fertilization to reduce rust susceptibility",
            "rice": "Maintain optimal water levels to reduce blast disease",
            "potato": "Hill up soil around plants to prevent tuber exposure to late blight",
            "soybean": "Inoculate seeds with rhizobium for better disease resistance",
        }

        crop_lower = crop_type.lower()
        for key, hint in crop_specific_hints.items():
            if key in crop_lower:
                measures.append({
                    "category": "Crop-Specific",
                    "measure": hint,
                    "priority": "Medium",
                })

        return measures

    def comprehensive_disease_risk(
        self,
        region: str,
        crop_type: str,
        year: int,
        climate_data: Dict[str, float],
    ) -> Dict[str, Any]:
        pest_prob = self.predict_pest_attack(region, crop_type, climate_data)
        disease_prob = self.predict_disease_outbreak(region, crop_type, climate_data)

        temp = climate_data.get("temperature", 25)
        rainfall = climate_data.get("rainfall", 800)

        heat_stress = max(0, (temp - 35) / 10) if temp > 35 else 0
        cold_stress = max(0, (5 - temp) / 10) if temp < 5 else 0

        overall_risk = 0.4 * pest_prob + 0.4 * disease_prob + 0.1 * heat_stress + 0.1 * cold_stress
        overall_risk = min(1.0, max(0.0, overall_risk))

        if overall_risk < 0.2:
            risk_level = "Very Low"
            action = "No action needed. Continue regular monitoring."
        elif overall_risk < 0.35:
            risk_level = "Low"
            action = "Routine monitoring recommended. Prepare preventive supplies."
        elif overall_risk < 0.5:
            risk_level = "Moderate"
            action = "Increase monitoring frequency. Apply preventive treatments."
        elif overall_risk < 0.7:
            risk_level = "High"
            action = "Immediate preventive action required. Intensify pest surveillance."
        else:
            risk_level = "Very High"
            action = "Emergency response needed. Deploy all available control measures immediately."

        top_pests = self.crop_pest_profiles.get(
            crop_type.lower(), {"pests": ["general_pests"]}
        )["pests"]

        top_diseases = self.crop_disease_profiles.get(
            crop_type.lower(), {"diseases": ["general_diseases"]}
        )["diseases"]

        preventive_measures = []
        for pest in top_pests:
            preventive_measures.extend(self.get_preventive_measures(pest, crop_type))

        season = self._determine_season(climate_data)
        seasonal_risk = self.assess_seasonal_risk(region, season)

        return {
            "region": region,
            "crop_type": crop_type,
            "year": year,
            "pest_attack_probability": pest_prob,
            "disease_outbreak_probability": disease_prob,
            "overall_risk_score": round(overall_risk, 4),
            "risk_level": risk_level,
            "recommended_action": action,
            "primary_threats": {
                "pests": [{"name": p, "probability": round(pest_prob * (0.8 + 0.2 * (len(top_pests) - i) / len(top_pests)), 4)} for i, p in enumerate(top_pests)],
                "diseases": [{"name": d, "probability": round(disease_prob * (0.8 + 0.2 * (len(top_diseases) - i) / len(top_diseases)), 4)} for i, d in enumerate(top_diseases)],
            },
            "climate_risk_factors": {
                "heat_stress": round(heat_stress, 4),
                "cold_stress": round(cold_stress, 4),
                "temperature": temp,
                "rainfall": rainfall,
                "humidity": climate_data.get("humidity", 60),
            },
            "seasonal_risk": seasonal_risk,
            "preventive_measures": preventive_measures[:8],
            "generated_at": datetime.now().isoformat(),
        }

    def predict_risk(
        self, region: str, crop_type: str, year: int
    ) -> Dict[str, Any]:
        climate_data = {
            "temperature": 25.0,
            "rainfall": 800.0,
            "humidity": 65.0,
        }
        result = self.comprehensive_disease_risk(region, crop_type, year, climate_data)
        return {
            "region": result["region"],
            "crop_type": result["crop_type"],
            "year": result["year"],
            "pest_attack_probability": result["pest_attack_probability"],
            "disease_outbreak_probability": result["disease_outbreak_probability"],
            "seasonal_risk": result["seasonal_risk"]["risk_level"],
            "preventive_measures": [m["measure"] for m in result["preventive_measures"]],
        }

    def predict_batch(
        self, payloads: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        results = []
        for payload in payloads:
            try:
                data = self.predict_risk(
                    region=payload["region"],
                    crop_type=payload["crop_type"],
                    year=payload["year"],
                )
                results.append({"status": "success", "data": data})
            except Exception:
                results.append({"status": "error", "data": None})
        return results

    def get_disease_history(
        self, region: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        crop_types = ["maize", "wheat", "rice", "potato", "soybean"]
        history = []
        for i in range(min(limit, 20)):
            crop = crop_types[i % len(crop_types)]
            year = 2024 - i
            climate_data = {
                "temperature": 20.0 + (i * 0.5) % 15,
                "rainfall": 600.0 + (i * 50) % 800,
                "humidity": 55.0 + (i * 3) % 35,
            }
            result = self.comprehensive_disease_risk(region, crop, year, climate_data)
            history.append({
                "region": result["region"],
                "crop_type": result["crop_type"],
                "year": result["year"],
                "pest_attack_probability": result["pest_attack_probability"],
                "disease_outbreak_probability": result["disease_outbreak_probability"],
                "seasonal_risk": result["seasonal_risk"]["risk_level"],
                "preventive_measures": [m["measure"] for m in result["preventive_measures"]],
            })
        return history[:limit]

    def _determine_season(self, climate_data: Dict[str, float]) -> str:
        temp = climate_data.get("temperature", 25)
        rainfall = climate_data.get("rainfall", 800)

        if temp > 30 and rainfall > 1000:
            return "monsoon"
        elif temp > 25:
            return "summer"
        elif 15 <= temp <= 25:
            return "spring" if rainfall > 500 else "autumn"
        else:
            return "winter"
