export const HEALTH_CATEGORIES = {
  EXCELLENT: { label: 'Excellent', min: 80, max: 100, color: '#16a34a', bg: 'bg-green-100', text: 'text-green-800' },
  GOOD: { label: 'Good', min: 60, max: 80, color: '#22c55e', bg: 'bg-green-50', text: 'text-green-700' },
  MODERATE: { label: 'Moderate', min: 40, max: 60, color: '#eab308', bg: 'bg-yellow-100', text: 'text-yellow-800' },
  POOR: { label: 'Poor', min: 20, max: 40, color: '#f97316', bg: 'bg-orange-100', text: 'text-orange-800' },
  CRITICAL: { label: 'Critical', min: 0, max: 20, color: '#ef4444', bg: 'bg-red-100', text: 'text-red-800' },
};

export const HEALTH_COLORS = ['#16a34a', '#22c55e', '#eab308', '#f97316', '#ef4444'];

export const getHealthCategory = (value) => {
  const categories = Object.values(HEALTH_CATEGORIES);
  return categories.find((c) => value >= c.min && value <= c.max) || HEALTH_CATEGORIES.MODERATE;
};

export const getHealthColor = (value) => getHealthCategory(value).color;

export const CHART_DEFAULTS = {
  ANIMATION_DURATION: 500,
  GRADIENT_ID: 'healthGradient',
  MARGIN: { top: 10, right: 10, left: 0, bottom: 0 },
};

export const CROP_TYPES = [
  { value: 'rice', label: 'Rice' },
  { value: 'wheat', label: 'Wheat' },
  { value: 'maize', label: 'Maize' },
  { value: 'sugarcane', label: 'Sugarcane' },
  { value: 'cotton', label: 'Cotton' },
  { value: 'jute', label: 'Jute' },
  { value: 'tea', label: 'Tea' },
  { value: 'coffee', label: 'Coffee' },
  { value: 'rubber', label: 'Rubber' },
  { value: 'coconut', label: 'Coconut' },
  { value: 'groundnut', label: 'Groundnut' },
  { value: 'pulses', label: 'Pulses' },
  { value: 'potato', label: 'Potato' },
  { value: 'onion', label: 'Onion' },
  { value: 'tomato', label: 'Tomato' },
];

export const REGIONS = [
  { value: 'north_india', label: 'North India' },
  { value: 'south_india', label: 'South India' },
  { value: 'east_india', label: 'East India' },
  { value: 'west_india', label: 'West India' },
  { value: 'central_india', label: 'Central India' },
  { value: 'north_east', label: 'North East India' },
];

export const SOIL_TYPES = [
  { value: 'alluvial', label: 'Alluvial' },
  { value: 'black', label: 'Black (Regur)' },
  { value: 'red', label: 'Red' },
  { value: 'laterite', label: 'Laterite' },
  { value: 'desert', label: 'Desert / Arid' },
  { value: 'mountain', label: 'Mountain / Forest' },
  { value: 'saline', label: 'Saline / Alkaline' },
  { value: 'peaty', label: 'Peaty / Marshy' },
];

export const SEASONS = [
  { value: 'kharif', label: 'Kharif (Monsoon)' },
  { value: 'rabi', label: 'Rabi (Winter)' },
  { value: 'zaid', label: 'Zaid (Summer)' },
];

export const CROP_HEALTH_INDICATORS = [
  { key: 'ndvi', label: 'NDVI (Vegetation Index)', min: 0, max: 1, unit: '' },
  { key: 'soil_moisture', label: 'Soil Moisture', min: 0, max: 100, unit: '%' },
  { key: 'temperature', label: 'Temperature', min: -10, max: 50, unit: '°C' },
  { key: 'rainfall', label: 'Rainfall', min: 0, max: 500, unit: 'mm' },
  { key: 'humidity', label: 'Humidity', min: 0, max: 100, unit: '%' },
  { key: 'ph_level', label: 'pH Level', min: 0, max: 14, unit: '' },
  { key: 'nitrogen', label: 'Nitrogen (N)', min: 0, max: 200, unit: 'kg/ha' },
  { key: 'phosphorus', label: 'Phosphorus (P)', min: 0, max: 200, unit: 'kg/ha' },
  { key: 'potassium', label: 'Potassium (K)', min: 0, max: 200, unit: 'kg/ha' },
];

export const DISEASE_TYPES = [
  { value: 'fungal', label: 'Fungal' },
  { value: 'bacterial', label: 'Bacterial' },
  { value: 'viral', label: 'Viral' },
  { value: 'pest', label: 'Pest Infestation' },
  { value: 'nutritional', label: 'Nutritional Deficiency' },
];

export const IRRIGATION_METHODS = [
  { value: 'drip', label: 'Drip Irrigation', efficiency: 90 },
  { value: 'sprinkler', label: 'Sprinkler Irrigation', efficiency: 75 },
  { value: 'flood', label: 'Flood Irrigation', efficiency: 50 },
  { value: 'furrow', label: 'Furrow Irrigation', efficiency: 60 },
  { value: 'pivot', label: 'Center Pivot', efficiency: 85 },
  { value: 'subsurface', label: 'Subsurface Drip', efficiency: 95 },
];

export const MONTHS = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
];
