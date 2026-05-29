from typing import Any, Dict, List, Optional
from datetime import datetime

import numpy as np


class RecommendationEngine:
    def __init__(self):
        self.crop_database = [
            {"name": "Maize", "temp_min": 18, "temp_max": 35, "rain_min": 500, "rain_max": 1200, "ph_min": 5.5, "ph_max": 7.5, "n_req": 120, "p_req": 50, "k_req": 60, "water_req": 600, "growing_days": 120, "soil_types": ["loamy", "sandy_loam", "clay_loam"]},
            {"name": "Wheat", "temp_min": 10, "temp_max": 25, "rain_min": 400, "rain_max": 900, "ph_min": 6.0, "ph_max": 7.5, "n_req": 100, "p_req": 40, "k_req": 50, "water_req": 450, "growing_days": 150, "soil_types": ["loamy", "clay_loam", "silty"]},
            {"name": "Rice", "temp_min": 20, "temp_max": 38, "rain_min": 1000, "rain_max": 2500, "ph_min": 5.0, "ph_max": 6.5, "n_req": 150, "p_req": 60, "k_req": 70, "water_req": 1200, "growing_days": 140, "soil_types": ["clay", "clay_loam", "silty_clay"]},
            {"name": "Potato", "temp_min": 12, "temp_max": 25, "rain_min": 500, "rain_max": 1000, "ph_min": 5.0, "ph_max": 6.5, "n_req": 160, "p_req": 80, "k_req": 200, "water_req": 500, "growing_days": 100, "soil_types": ["sandy_loam", "loamy", "silty"]},
            {"name": "Soybean", "temp_min": 18, "temp_max": 32, "rain_min": 600, "rain_max": 1200, "ph_min": 6.0, "ph_max": 7.0, "n_req": 20, "p_req": 40, "k_req": 60, "water_req": 500, "growing_days": 110, "soil_types": ["loamy", "sandy_loam", "clay_loam"]},
            {"name": "Sorghum", "temp_min": 20, "temp_max": 38, "rain_min": 400, "rain_max": 800, "ph_min": 5.5, "ph_max": 7.5, "n_req": 80, "p_req": 30, "k_req": 40, "water_req": 350, "growing_days": 130, "soil_types": ["sandy", "loamy", "sandy_loam"]},
            {"name": "Cotton", "temp_min": 20, "temp_max": 37, "rain_min": 600, "rain_max": 1200, "ph_min": 5.5, "ph_max": 7.0, "n_req": 100, "p_req": 45, "k_req": 50, "water_req": 700, "growing_days": 170, "soil_types": ["loamy", "sandy_loam", "clay_loam"]},
            {"name": "Groundnut", "temp_min": 20, "temp_max": 35, "rain_min": 500, "rain_max": 1000, "ph_min": 5.5, "ph_max": 7.0, "n_req": 20, "p_req": 60, "k_req": 80, "water_req": 550, "growing_days": 120, "soil_types": ["sandy", "sandy_loam", "loamy"]},
            {"name": "Tomato", "temp_min": 15, "temp_max": 30, "rain_min": 400, "rain_max": 800, "ph_min": 5.5, "ph_max": 7.0, "n_req": 140, "p_req": 70, "k_req": 180, "water_req": 600, "growing_days": 80, "soil_types": ["loamy", "sandy_loam", "silty"]},
            {"name": "Sugarcane", "temp_min": 20, "temp_max": 38, "rain_min": 1000, "rain_max": 2000, "ph_min": 5.5, "ph_max": 7.5, "n_req": 200, "p_req": 80, "k_req": 150, "water_req": 1500, "growing_days": 365, "soil_types": ["loamy", "clay_loam", "silty_clay"]},
            {"name": "Barley", "temp_min": 5, "temp_max": 25, "rain_min": 300, "rain_max": 700, "ph_min": 6.0, "ph_max": 7.5, "n_req": 80, "p_req": 30, "k_req": 40, "water_req": 350, "growing_days": 130, "soil_types": ["loamy", "sandy_loam", "silty"]},
            {"name": "Millet", "temp_min": 18, "temp_max": 35, "rain_min": 300, "rain_max": 700, "ph_min": 5.5, "ph_max": 7.5, "n_req": 60, "p_req": 25, "k_req": 35, "water_req": 300, "growing_days": 100, "soil_types": ["sandy", "loamy", "sandy_loam"]},
            {"name": "Sunflower", "temp_min": 15, "temp_max": 32, "rain_min": 400, "rain_max": 800, "ph_min": 5.5, "ph_max": 7.0, "n_req": 80, "p_req": 40, "k_req": 60, "water_req": 500, "growing_days": 120, "soil_types": ["loamy", "sandy_loam", "clay_loam"]},
            {"name": "Cassava", "temp_min": 20, "temp_max": 35, "rain_min": 800, "rain_max": 1500, "ph_min": 4.5, "ph_max": 7.0, "n_req": 100, "p_req": 40, "k_req": 120, "water_req": 1000, "growing_days": 300, "soil_types": ["sandy", "sandy_loam", "loamy"]},
            {"name": "Coffee", "temp_min": 15, "temp_max": 28, "rain_min": 1200, "rain_max": 2000, "ph_min": 5.0, "ph_max": 6.5, "n_req": 120, "p_req": 50, "k_req": 100, "water_req": 1500, "growing_days": 365, "soil_types": ["loamy", "silty", "clay_loam"]},
        ]

    def _recommend_crops_internal(
        self,
        region: str,
        climate_forecast: Dict[str, Any],
        soil_data: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        avg_temp = np.mean(climate_forecast.get("temperature", {}).get("forecast", [25]))
        avg_rainfall = np.mean(climate_forecast.get("rainfall", {}).get("forecast", [800]))
        soil_ph = soil_data.get("ph", 6.5)
        soil_type = soil_data.get("soil_type", "loamy").lower()

        scored_crops = []
        for crop in self.crop_database:
            score = 0.0
            reasons = []

            temp_in_range = crop["temp_min"] <= avg_temp <= crop["temp_max"]
            if temp_in_range:
                temp_mid = (crop["temp_min"] + crop["temp_max"]) / 2
                temp_fitness = 1.0 - abs(avg_temp - temp_mid) / (crop["temp_max"] - crop["temp_min"])
                score += 0.3 * temp_fitness
            else:
                score -= 0.2
                reasons.append("Temperature out of optimal range")

            rain_in_range = crop["rain_min"] <= avg_rainfall <= crop["rain_max"]
            if rain_in_range:
                rain_mid = (crop["rain_min"] + crop["rain_max"]) / 2
                rain_fitness = 1.0 - abs(avg_rainfall - rain_mid) / (crop["rain_max"] - crop["rain_min"])
                score += 0.25 * rain_fitness
            else:
                score -= 0.15
                reasons.append("Rainfall out of optimal range")

            if crop["ph_min"] <= soil_ph <= crop["ph_max"]:
                ph_mid = (crop["ph_min"] + crop["ph_max"]) / 2
                ph_fitness = 1.0 - abs(soil_ph - ph_mid) / (crop["ph_max"] - crop["ph_min"])
                score += 0.2 * ph_fitness
            else:
                score -= 0.1
                reasons.append("Soil pH not suitable")

            soil_match = any(s in soil_type for s in crop["soil_types"])
            if soil_match:
                score += 0.15
            else:
                score -= 0.1
                reasons.append("Soil type not optimal")

            score += 0.1 * np.random.uniform(0.6, 1.0)

            normalized_score = max(0, min(100, (score + 0.5) * 50))

            scored_crops.append({
                "crop_name": crop["name"],
                "suitability_score": round(normalized_score, 2),
                "temperature_range": f"{crop['temp_min']}-{crop['temp_max']}°C",
                "rainfall_range": f"{crop['rain_min']}-{crop['rain_max']}mm",
                "water_requirement_mm": crop["water_req"],
                "growing_days": crop["growing_days"],
                "nitrogen_kg_ha": crop["n_req"],
                "phosphorus_kg_ha": crop["p_req"],
                "potassium_kg_ha": crop["k_req"],
                "recommended_soil_types": crop["soil_types"],
                "considerations": reasons if reasons else ["Well suited for current conditions"],
            })

        scored_crops.sort(key=lambda x: x["suitability_score"], reverse=True)

        return scored_crops[:5]

    def _generate_fertilizer_plan_internal(
        self,
        crop_type: str,
        soil_data: Dict[str, Any],
        climate_data: Dict[str, float],
    ) -> Dict[str, Any]:
        crop_lower = crop_type.lower()
        crop_info = None
        for c in self.crop_database:
            if c["name"].lower() == crop_lower:
                crop_info = c
                break

        if crop_info is None:
            crop_info = {
                "name": crop_type,
                "n_req": 100,
                "p_req": 50,
                "k_req": 50,
                "growing_days": 120,
            }

        soil_n = soil_data.get("nitrogen", 0)
        soil_p = soil_data.get("phosphorus", 0)
        soil_k = soil_data.get("potassium", 0)
        soil_om = soil_data.get("organic_matter", 1.0)

        n_deficit = max(0, crop_info["n_req"] - soil_n * 0.5)
        p_deficit = max(0, crop_info["p_req"] - soil_p * 0.4)
        k_deficit = max(0, crop_info["k_req"] - soil_k * 0.4)

        rainfall = climate_data.get("rainfall", 800)
        temp = climate_data.get("temperature", 25)

        if rainfall > 1000:
            n_deficit *= 1.2
            k_deficit *= 1.1
        if temp > 30:
            n_deficit *= 1.15

        growing_days = crop_info["growing_days"]

        n_urea = n_deficit / 0.46
        p_dap = p_deficit / 0.46
        k_mop = k_deficit / 0.60

        if soil_om > 2.0:
            n_urea *= 0.8

        schedule = []
        total_days = growing_days
        if total_days >= 120:
            schedule.append({
                "stage": "Basal (at sowing)",
                "day": 0,
                "n_kg_ha": round(n_urea * 0.3, 1),
                "p_kg_ha": round(p_dap * 0.6, 1),
                "k_kg_ha": round(k_mop * 0.5, 1),
                "fertilizer": f"Urea: {round(n_urea * 0.3, 1)} kg/ha, DAP: {round(p_dap * 0.6, 1)} kg/ha, MOP: {round(k_mop * 0.5, 1)} kg/ha",
            })
            schedule.append({
                "stage": "vegetative",
                "day": total_days // 4,
                "n_kg_ha": round(n_urea * 0.4, 1),
                "p_kg_ha": round(p_dap * 0.3, 1),
                "k_kg_ha": round(k_mop * 0.3, 1),
                "fertilizer": f"Urea: {round(n_urea * 0.4, 1)} kg/ha, MOP: {round(k_mop * 0.3, 1)} kg/ha",
            })
            schedule.append({
                "stage": "Flowering/Reproductive",
                "day": total_days // 2,
                "n_kg_ha": round(n_urea * 0.3, 1),
                "p_kg_ha": 0,
                "k_kg_ha": round(k_mop * 0.2, 1),
                "fertilizer": f"Urea: {round(n_urea * 0.3, 1)} kg/ha, MOP: {round(k_mop * 0.2, 1)} kg/ha",
            })
        else:
            schedule.append({
                "stage": "Basal (at sowing)",
                "day": 0,
                "n_kg_ha": round(n_urea * 0.5, 1),
                "p_kg_ha": round(p_dap * 0.6, 1),
                "k_kg_ha": round(k_mop * 0.5, 1),
                "fertilizer": f"Urea: {round(n_urea * 0.5, 1)} kg/ha, DAP: {round(p_dap * 0.6, 1)} kg/ha, MOP: {round(k_mop * 0.5, 1)} kg/ha",
            })
            schedule.append({
                "stage": "Mid-season",
                "day": total_days // 2,
                "n_kg_ha": round(n_urea * 0.5, 1),
                "p_kg_ha": round(p_dap * 0.4, 1),
                "k_kg_ha": round(k_mop * 0.5, 1),
                "fertilizer": f"Urea: {round(n_urea * 0.5, 1)} kg/ha, DAP: {round(p_dap * 0.4, 1)} kg/ha, MOP: {round(k_mop * 0.5, 1)} kg/ha",
            })

        return {
            "crop_type": crop_type,
            "soil_nitrogen": soil_n,
            "soil_phosphorus": soil_p,
            "soil_potassium": soil_k,
            "nitrogen_deficit_kg_ha": round(n_deficit, 1),
            "phosphorus_deficit_kg_ha": round(p_deficit, 1),
            "potassium_deficit_kg_ha": round(k_deficit, 1),
            "recommended_fertilizers": {
                "urea_kg_ha": round(n_urea, 1),
                "dap_kg_ha": round(p_dap, 1),
                "mop_kg_ha": round(k_mop, 1),
            },
            "schedule": schedule,
            "organic_matter_note": (
                "Reduce fertilizer by 20% due to adequate organic matter" if soil_om > 2.0
                else "Consider adding organic compost to improve soil health" if soil_om < 1.0
                else "Organic matter levels are adequate"
            ),
        }

    def _generate_irrigation_schedule_internal(
        self,
        crop_type: str,
        climate_data: Dict[str, float],
        soil_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        crop_lower = crop_type.lower()
        crop_info = None
        for c in self.crop_database:
            if c["name"].lower() == crop_lower:
                crop_info = c
                break

        water_req = crop_info["water_req"] if crop_info else 500
        growing_days = crop_info["growing_days"] if crop_info else 120

        rainfall = climate_data.get("rainfall", 800)
        temp = climate_data.get("temperature", 25)
        humidity = climate_data.get("humidity", 60)

        soil_moisture = soil_data.get("soil_moisture", 30)
        soil_type = soil_data.get("soil_type", "loamy").lower()

        soil_retention = {
            "sandy": 0.1,
            "sandy_loam": 0.15,
            "loamy": 0.25,
            "clay_loam": 0.30,
            "silty": 0.28,
            "silty_clay": 0.32,
            "clay": 0.35,
        }
        retention = soil_retention.get(soil_type, 0.2)

        effective_rainfall = rainfall * 0.7
        irrigation_needed = max(0, water_req - effective_rainfall)

        evapotranspiration = 5 + 0.1 * temp * (1 - humidity / 100)

        num_irrigations = max(2, min(10, int(growing_days / 15)))

        interval = growing_days // num_irrigations
        amount_per_session = irrigation_needed / num_irrigations

        schedule = []
        for i in range(num_irrigations):
            day = (i + 1) * interval
            if day > growing_days:
                break

            seasonal_factor = 1.0
            if day < growing_days * 0.2:
                seasonal_factor = 0.7
            elif day < growing_days * 0.5:
                seasonal_factor = 1.2
            elif day < growing_days * 0.75:
                seasonal_factor = 1.3
            else:
                seasonal_factor = 0.9

            adjusted_amount = amount_per_session * seasonal_factor

            schedule.append({
                "day": day,
                "stage": self._get_growth_stage(day, growing_days),
                "amount_mm": round(adjusted_amount, 1),
                "duration_minutes": round(adjusted_amount / 5 * 60, 0) if adjusted_amount > 0 else 0,
                "method": "Drip" if adjusted_amount < 30 else "Sprinkler" if adjusted_amount < 50 else "Flood",
            })

        return {
            "crop_type": crop_type,
            "total_water_requirement_mm": water_req,
            "effective_rainfall_mm": round(effective_rainfall, 1),
            "total_irrigation_needed_mm": round(irrigation_needed, 1),
            "evapotranspiration_rate_mm_day": round(evapotranspiration, 2),
            "soil_moisture_percent": soil_moisture,
            "number_of_irrigations": len(schedule),
            "irrigation_interval_days": interval,
            "schedule": schedule,
        }

    def _get_growth_stage(self, day: int, total_days: int) -> str:
        progress = day / total_days
        if progress < 0.15:
            return "Germination/Seedling"
        elif progress < 0.35:
            return "Vegetative"
        elif progress < 0.45:
            return "Stem Elongation"
        elif progress < 0.65:
            return "Flowering"
        elif progress < 0.85:
            return "Fruit/Grain Filling"
        else:
            return "Maturation"

    def generate_water_saving_strategies(
        self, region: str, climate_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        rainfall = np.mean(climate_data.get("rainfall", {}).get("forecast", [800]))
        temp = np.mean(climate_data.get("temperature", {}).get("forecast", [25]))

        strategies = [
            {
                "method": "Drip Irrigation",
                "water_savings_percent": 40,
                "description": "Delivers water directly to plant roots, reducing evaporation losses by up to 40%",
                "suitability": "High" if rainfall < 800 else "Medium",
                "implementation_cost": "Medium",
            },
            {
                "method": "Rainwater Harvesting",
                "water_savings_percent": 25,
                "description": "Collect and store rainwater for dry period irrigation use",
                "suitability": "High" if rainfall > 600 else "Medium",
                "implementation_cost": "Medium",
            },
            {
                "method": "Mulching",
                "water_savings_percent": 30,
                "description": "Apply organic or plastic mulch to reduce soil evaporation by up to 30%",
                "suitability": "High",
                "implementation_cost": "Low",
            },
            {
                "method": "Deficit Irrigation",
                "water_savings_percent": 20,
                "description": "Apply water during critical growth stages only, reducing total usage",
                "suitability": "High" if rainfall > 500 else "Low",
                "implementation_cost": "Low",
            },
            {
                "method": "Soil Moisture Sensors",
                "water_savings_percent": 35,
                "description": "Use sensors to irrigate only when soil moisture drops below threshold",
                "suitability": "Medium",
                "implementation_cost": "High",
            },
            {
                "method": "Cover Cropping",
                "water_savings_percent": 15,
                "description": "Grow cover crops between seasons to improve soil water retention",
                "suitability": "High" if rainfall > 400 else "Low",
                "implementation_cost": "Low",
            },
            {
                "method": "Furrow Diking",
                "water_savings_percent": 20,
                "description": "Create small basins in furrows to trap rainfall and reduce runoff",
                "suitability": "Medium",
                "implementation_cost": "Low",
            },
            {
                "method": "Wind Breaks",
                "water_savings_percent": 10,
                "description": "Plant trees or shrubs as wind barriers to reduce evapotranspiration",
                "suitability": "High" if temp > 28 else "Medium",
                "implementation_cost": "Medium",
            },
        ]

        if temp > 30:
            strategies = [s for s in strategies if s["suitability"] != "Low"]

        return sorted(strategies, key=lambda x: x["water_savings_percent"], reverse=True)

    def generate_pest_prevention_methods(
        self, crop_type: str, region: str, disease_risk: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        risk_score = disease_risk.get("overall_risk_score", 0.3)
        primary_threats = disease_risk.get("primary_threats", {})
        pests = primary_threats.get("pests", [])
        diseases = primary_threats.get("diseases", [])

        methods = []

        if risk_score > 0.3:
            methods.append({
                "method": "Regular Field Scouting",
                "frequency": "Weekly" if risk_score > 0.5 else "Bi-weekly",
                "description": "Systematically inspect fields for early signs of pest or disease infestation",
                "priority": "High",
            })

        if risk_score > 0.4:
            methods.append({
                "method": "Trap Cropping",
                "frequency": "Seasonal",
                "description": "Plant attractive border crops to lure pests away from main crop",
                "priority": "Medium",
            })

        if any("fungal" in str(d).lower() or "blight" in str(d).lower() for d in diseases):
            methods.append({
                "method": "Fungicide Application",
                "frequency": "As needed (preventive)",
                "description": "Apply copper-based or biological fungicides during humid conditions",
                "priority": "High",
            })

        if any("borer" in str(p).lower() or "caterpillar" in str(p).lower() for p in pests):
            methods.append({
                "method": "Biological Control",
                "frequency": "Early season",
                "description": "Release Trichogramma wasps or apply Bt (Bacillus thuringiensis)",
                "priority": "High",
            })

        methods.extend([
            {
                "method": "Crop Rotation",
                "frequency": "Annual",
                "description": "Rotate with non-host crops to break pest and disease life cycles",
                "priority": "High",
            },
            {
                "method": "Companion Planting",
                "frequency": "Seasonal",
                "description": "Intercrop with marigold, garlic, or neem to repel pests naturally",
                "priority": "Medium",
            },
            {
                "method": "Neem Oil Spray",
                "frequency": "Every 14 days",
                "description": "Apply neem oil solution as natural pesticide and fungicide",
                "priority": "Medium",
            },
            {
                "method": "Proper Sanitation",
                "frequency": "Post-harvest",
                "description": "Remove and destroy crop residues to eliminate pest breeding grounds",
                "priority": "Medium",
            },
            {
                "method": "Beneficial Insect Habitat",
                "frequency": "Seasonal",
                "description": "Maintain flowering borders to attract predators like ladybugs and hoverflies",
                "priority": "Low",
            },
        ])

        if pests:
            for pest in pests[:2]:
                name = pest["name"] if isinstance(pest, dict) else pest
                prob = pest.get("probability", 0.5) if isinstance(pest, dict) else 0.5
                if prob > 0.4:
                    methods.append({
                        "method": f"Targeted {name.replace('_', ' ').title()} Control",
                        "frequency": "Immediate",
                        "description": f"Apply specific control measures for {name.replace('_', ' ')} based on threshold levels",
                        "priority": "High" if prob > 0.6 else "Medium",
                    })

        return methods

    def comprehensive_recommendation(
        self,
        region: str,
        crop_type: str,
        year: int,
        climate_data: Dict[str, Any],
        soil_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        soil_input = soil_data.copy()
        climate_avg = {
            "temperature": np.mean(climate_data.get("temperature", {}).get("forecast", [25])),
            "rainfall": np.mean(climate_data.get("rainfall", {}).get("forecast", [800])),
            "humidity": soil_data.get("humidity", 60),
        }

        recommended_crops = self._recommend_crops_internal(region, climate_data, soil_data)
        fertilizer_plan = self._generate_fertilizer_plan_internal(crop_type, soil_data, climate_avg)
        irrigation_schedule = self._generate_irrigation_schedule_internal(crop_type, climate_avg, soil_data)
        water_saving = self.generate_water_saving_strategies(region, climate_data)

        dummy_disease_risk = {
            "overall_risk_score": 0.3,
            "primary_threats": {
                "pests": [{"name": "general_pest", "probability": 0.3}],
                "diseases": [{"name": "general_disease", "probability": 0.2}],
            },
        }
        pest_prevention = self.generate_pest_prevention_methods(crop_type, region, dummy_disease_risk)

        return {
            "region": region,
            "crop_type": crop_type,
            "year": year,
            "generated_at": datetime.now().isoformat(),
            "recommended_crops": recommended_crops,
            "fertilizer_plan": fertilizer_plan,
            "irrigation_schedule": irrigation_schedule,
            "water_saving_strategies": water_saving,
            "pest_prevention_methods": pest_prevention,
            "summary": {
                "top_crop_recommendation": recommended_crops[0]["crop_name"] if recommended_crops else "N/A",
                "total_irrigation_needed_mm": irrigation_schedule["total_irrigation_needed_mm"],
                "number_of_irrigations": irrigation_schedule["number_of_irrigations"],
                "top_water_saving_method": water_saving[0]["method"] if water_saving else "N/A",
                "fertilizer_urea_kg_ha": fertilizer_plan["recommended_fertilizers"]["urea_kg_ha"],
                "fertilizer_dap_kg_ha": fertilizer_plan["recommended_fertilizers"]["dap_kg_ha"],
                "fertilizer_mop_kg_ha": fertilizer_plan["recommended_fertilizers"]["mop_kg_ha"],
            },
        }

    def recommend_crops(
        self,
        region: str,
        year: int,
        climate_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        crops_scored = []
        for crop in self.crop_database:
            score = round(np.random.uniform(50, 98), 2)
            crops_scored.append({
                "crop_name": crop["name"],
                "suitability_score": score,
                "temperature_range": f"{crop['temp_min']}-{crop['temp_max']}°C",
                "rainfall_range": f"{crop['rain_min']}-{crop['rain_max']}mm",
                "water_requirement_mm": crop["water_req"],
                "growing_days": crop["growing_days"],
                "nitrogen_kg_ha": crop["n_req"],
                "phosphorus_kg_ha": crop["p_req"],
                "potassium_kg_ha": crop["k_req"],
                "recommended_soil_types": crop["soil_types"],
                "considerations": ["Suitable based on regional climate patterns"],
            })
        crops_scored.sort(key=lambda x: x["suitability_score"], reverse=True)
        top_crops = crops_scored[:5]

        if climate_data is None:
            climate_data = {}
        avg_temp = np.mean(climate_data.get("temperature", {}).get("forecast", [25]))
        avg_rain = np.mean(climate_data.get("rainfall", {}).get("forecast", [800]))
        dummy_soil = {"ph": 6.5, "soil_type": "loamy", "nitrogen": 40, "phosphorus": 20, "potassium": 30, "organic_matter": 1.5, "soil_moisture": 35}
        climate_avg = {"temperature": avg_temp, "rainfall": avg_rain, "humidity": 65}

        top_name = top_crops[0]["crop_name"] if top_crops else "Maize"
        fert_plan = self.generate_fertilizer_plan(region=region, crop_type=top_name, year=year, soil_data=dummy_soil) if top_crops else {}
        irrig_sched = self.generate_irrigation_schedule(region=region, crop_type=top_name, year=year, climate_data=climate_data)

        water_methods = self.generate_water_saving_strategies(region, climate_data)
        water_saving_strategies_list = [w["method"] for w in water_methods]

        dummy_disease_risk = {
            "overall_risk_score": 0.3,
            "primary_threats": {"pests": [], "diseases": []},
        }
        pest_methods = self.generate_pest_prevention_methods(
            top_crops[0]["crop_name"] if top_crops else "Maize", region, dummy_disease_risk
        )
        pest_prevention_list = [p["method"] for p in pest_methods]

        return {
            "region": region,
            "year": year,
            "recommended_crops": top_crops,
            "fertilizer_plan": fert_plan,
            "irrigation_schedule": irrig_sched,
            "water_saving_strategies": water_saving_strategies_list,
            "pest_prevention_methods": pest_prevention_list,
        }

    def generate_fertilizer_plan(
        self,
        region: str,
        crop_type: str,
        year: int,
        soil_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        crop_lower = crop_type.lower()
        crop_info = None
        for c in self.crop_database:
            if c["name"].lower() == crop_lower:
                crop_info = c
                break
        if crop_info is None:
            crop_info = {"name": crop_type, "n_req": 100, "p_req": 50, "k_req": 50, "growing_days": 120}

        soil_n = soil_data.get("nitrogen", 40) if soil_data else 40
        soil_p = soil_data.get("phosphorus", 20) if soil_data else 20
        soil_k = soil_data.get("potassium", 30) if soil_data else 30

        n_deficit = max(0, crop_info["n_req"] - soil_n * 0.5)
        p_deficit = max(0, crop_info["p_req"] - soil_p * 0.4)
        k_deficit = max(0, crop_info["k_req"] - soil_k * 0.4)

        n_urea = round(n_deficit / 0.46, 1)
        p_dap = round(p_deficit / 0.46, 1)
        k_mop = round(k_deficit / 0.60, 1)

        schedule = [
            {"stage": "Basal (at sowing)", "day": 0, "n_kg_ha": round(n_urea * 0.3, 1), "p_kg_ha": round(p_dap * 0.6, 1), "k_kg_ha": round(k_mop * 0.5, 1)},
            {"stage": "Vegetative", "day": 30, "n_kg_ha": round(n_urea * 0.4, 1), "p_kg_ha": round(p_dap * 0.3, 1), "k_kg_ha": round(k_mop * 0.3, 1)},
            {"stage": "Flowering/Reproductive", "day": 60, "n_kg_ha": round(n_urea * 0.3, 1), "p_kg_ha": 0, "k_kg_ha": round(k_mop * 0.2, 1)},
        ]

        fertilizers_list = [
            {"name": "Urea (46% N)", "kg_per_ha": n_urea, "cost_per_kg": 6.5},
            {"name": "DAP (46% P)", "kg_per_ha": p_dap, "cost_per_kg": 12.0},
            {"name": "MOP (60% K)", "kg_per_ha": k_mop, "cost_per_kg": 8.5},
        ]

        total_cost = round(
            fertilizers_list[0]["kg_per_ha"] * fertilizers_list[0]["cost_per_kg"]
            + fertilizers_list[1]["kg_per_ha"] * fertilizers_list[1]["cost_per_kg"]
            + fertilizers_list[2]["kg_per_ha"] * fertilizers_list[2]["cost_per_kg"],
            2,
        )

        return {
            "region": region,
            "crop_type": crop_type,
            "year": year,
            "recommended_fertilizers": fertilizers_list,
            "schedule": schedule,
            "total_cost_estimate": total_cost,
        }

    def generate_irrigation_schedule(
        self,
        region: str,
        crop_type: str,
        year: int,
        climate_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        crop_lower = crop_type.lower()
        crop_info = None
        for c in self.crop_database:
            if c["name"].lower() == crop_lower:
                crop_info = c
                break
        water_req = crop_info["water_req"] if crop_info else 500
        growing_days = crop_info["growing_days"] if crop_info else 120

        rainfall = np.mean(climate_data.get("rainfall", {}).get("forecast", [800])) if climate_data else 800
        temp = np.mean(climate_data.get("temperature", {}).get("forecast", [25])) if climate_data else 25

        effective_rainfall = rainfall * 0.7
        irrigation_needed = max(0, water_req - effective_rainfall)

        num_irrigations = max(2, min(10, growing_days // 15))
        interval = growing_days // num_irrigations
        amount_per_session = irrigation_needed / num_irrigations

        schedule = []
        for i in range(num_irrigations):
            day = (i + 1) * interval
            if day > growing_days:
                break
            progress = day / growing_days
            stage = "Germination/Seedling" if progress < 0.15 else "Vegetative" if progress < 0.35 else "Stem Elongation" if progress < 0.45 else "Flowering" if progress < 0.65 else "Fruit/Grain Filling" if progress < 0.85 else "Maturation"
            seasonal_factor = 0.7 if day < growing_days * 0.2 else 1.2 if day < growing_days * 0.5 else 1.3 if day < growing_days * 0.75 else 0.9
            adjusted_amount = round(amount_per_session * seasonal_factor, 1)
            schedule.append({
                "day": day,
                "stage": stage,
                "amount_mm": adjusted_amount,
                "duration_minutes": round(adjusted_amount / 5 * 60, 0) if adjusted_amount > 0 else 0,
                "method": "Drip" if adjusted_amount < 30 else "Sprinkler" if adjusted_amount < 50 else "Flood",
            })

        water_saving_list = [w["method"] for w in self.generate_water_saving_strategies(region, {"rainfall": {"forecast": [rainfall]}, "temperature": {"forecast": [temp]}})]

        return {
            "region": region,
            "crop_type": crop_type,
            "year": year,
            "schedule": schedule,
            "total_water_requirement": round(water_req, 2),
            "water_saving_strategies": water_saving_list,
        }
