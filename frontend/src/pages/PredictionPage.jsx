import React, { useState } from 'react';
import { toast } from 'react-toastify';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import HealthGauge from '../components/dashboard/HealthGauge';
import BarChart from '../components/charts/BarChart';
import { predictCropHealth } from '../services/predictionService';
import { CROP_TYPES, REGIONS, getHealthCategory } from '../utils/constants';

const schema = z.object({
  region: z.string().min(1, 'Region is required'),
  crop_type: z.string().min(1, 'Crop type is required'),
  season: z.string().min(1),
  area_hectares: z.string().min(1, 'Area is required'),
  rainfall: z.string().min(1),
  temperature: z.string().min(1),
  humidity: z.string().min(1),
  soil_moisture: z.string().min(1),
  ph_level: z.string().min(1),
  nitrogen: z.string().min(1),
  phosphorus: z.string().min(1),
  potassium: z.string().min(1),
});

export default function PredictionPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
    defaultValues: {
      season: 'kharif',
      rainfall: '850',
      temperature: '28',
      humidity: '65',
      soil_moisture: '45',
      ph_level: '6.5',
      nitrogen: '80',
      phosphorus: '40',
      potassium: '60',
    },
  });

  const onSubmit = async (data) => {
    try {
      setLoading(true);
      setResult(null);
      const numericData = Object.fromEntries(
        Object.entries(data).map(([k, v]) => [k, isNaN(v) ? v : parseFloat(v)])
      );
      const response = await predictCropHealth(numericData);
      setResult(response);
      toast.success('Prediction completed successfully!');
    } catch (err) {
      toast.error(err.message || 'Prediction failed');
      setResult(getMockResult(data));
    } finally {
      setLoading(false);
    }
  };

  const getMockResult = (data) => ({
    health_index: 45 + Math.random() * 45,
    yield_forecast: 3.2 + Math.random() * 4,
    risk_score: Math.random() * 100,
    confidence: 70 + Math.random() * 25,
    risk_level: Math.random() > 0.6 ? 'Low' : Math.random() > 0.3 ? 'Moderate' : 'High',
    feature_importance: [
      { feature: 'Rainfall', importance: 0.28 },
      { feature: 'Temperature', importance: 0.22 },
      { feature: 'Soil Moisture', importance: 0.18 },
      { feature: 'Nitrogen', importance: 0.12 },
      { feature: 'Humidity', importance: 0.10 },
      { feature: 'pH Level', importance: 0.06 },
      { feature: 'Phosphorus', importance: 0.03 },
      { feature: 'Potassium', importance: 0.01 },
    ],
    shap_explanations: [
      { feature: 'Rainfall', value: '850 mm', impact: '+12.5', color: 'positive' },
      { feature: 'Temperature', value: '28°C', impact: '+8.3', color: 'positive' },
      { feature: 'Nitrogen', value: '80 kg/ha', impact: '-3.2', color: 'negative' },
      { feature: 'Soil Moisture', value: '45%', impact: '+5.7', color: 'positive' },
    ],
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Crop Health Prediction</h1>
        <p className="text-sm text-gray-500 mt-1">Analyze crop health using environmental and soil parameters</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Input Parameters</h2>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Region</label>
                <select {...register('region')} className="select-field">
                  <option value="">Select region</option>
                  {REGIONS.map((r) => <option key={r.value} value={r.value}>{r.label}</option>)}
                </select>
                {errors.region && <p className="text-xs text-red-500 mt-1">{errors.region.message}</p>}
              </div>
              <div>
                <label className="label">Crop Type</label>
                <select {...register('crop_type')} className="select-field">
                  <option value="">Select crop</option>
                  {CROP_TYPES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
                </select>
                {errors.crop_type && <p className="text-xs text-red-500 mt-1">{errors.crop_type.message}</p>}
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="label">Season</label>
                <select {...register('season')} className="select-field">
                  <option value="kharif">Kharif</option>
                  <option value="rabi">Rabi</option>
                  <option value="zaid">Zaid</option>
                </select>
              </div>
              <div>
                <label className="label">Area (hectares)</label>
                <input type="number" step="0.1" {...register('area_hectares')} className="input-field" placeholder="e.g. 5" />
                {errors.area_hectares && <p className="text-xs text-red-500 mt-1">{errors.area_hectares.message}</p>}
              </div>
              <div>
                <label className="label">Rainfall (mm)</label>
                <input type="number" step="0.1" {...register('rainfall')} className="input-field" />
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="label">Temperature (°C)</label>
                <input type="number" step="0.1" {...register('temperature')} className="input-field" />
              </div>
              <div>
                <label className="label">Humidity (%)</label>
                <input type="number" step="0.1" {...register('humidity')} className="input-field" />
              </div>
              <div>
                <label className="label">Soil Moisture (%)</label>
                <input type="number" step="0.1" {...register('soil_moisture')} className="input-field" />
              </div>
            </div>

            <div className="grid grid-cols-4 gap-4">
              <div>
                <label className="label">pH Level</label>
                <input type="number" step="0.1" {...register('ph_level')} className="input-field" />
              </div>
              <div>
                <label className="label">Nitrogen (N)</label>
                <input type="number" step="0.1" {...register('nitrogen')} className="input-field" />
              </div>
              <div>
                <label className="label">Phosphorus (P)</label>
                <input type="number" step="0.1" {...register('phosphorus')} className="input-field" />
              </div>
              <div>
                <label className="label">Potassium (K)</label>
                <input type="number" step="0.1" {...register('potassium')} className="input-field" />
              </div>
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full py-2.5">
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Processing...
                </span>
              ) : (
                'Run Prediction'
              )}
            </button>
          </form>
        </div>

        <div className="space-y-6">
          {result ? (
            <>
              <div className="card">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Prediction Results</h2>
                <div className="flex flex-col items-center mb-4">
                  <HealthGauge value={result.health_index} size="lg" />
                </div>
                <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-gray-100">
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <p className="text-xs text-gray-500">Yield Forecast</p>
                    <p className="text-lg font-bold text-gray-900">{result.yield_forecast?.toFixed(2)} t/ha</p>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <p className="text-xs text-gray-500">Risk Score</p>
                    <p className={`text-lg font-bold ${
                      result.risk_score < 30 ? 'text-green-600' : result.risk_score < 60 ? 'text-yellow-600' : 'text-red-600'
                    }`}>
                      {result.risk_score?.toFixed(1)}%
                    </p>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <p className="text-xs text-gray-500">Confidence</p>
                    <p className="text-lg font-bold text-primary-600">{result.confidence?.toFixed(1)}%</p>
                  </div>
                </div>
                <div className="mt-4">
                  <span className={`badge ${
                    result.risk_level === 'Low' ? 'badge-green' : result.risk_level === 'Moderate' ? 'badge-yellow' : 'badge-red'
                  }`}>
                    {result.risk_level} Risk
                  </span>
                </div>
              </div>

              <div className="card">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Feature Importance</h2>
                <BarChart
                  data={result.feature_importance}
                  bars={[{ dataKey: 'importance', name: 'Importance' }]}
                  xKey="feature"
                  height={200}
                  horizontal
                  colors={['#22c55e']}
                />
              </div>

              <div className="card">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">SHAP Explanation</h2>
                <div className="space-y-2">
                  {result.shap_explanations.map((exp, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div>
                        <p className="text-sm font-medium text-gray-800">{exp.feature}</p>
                        <p className="text-xs text-gray-500">{exp.value}</p>
                      </div>
                      <span className={`text-sm font-semibold ${
                        exp.color === 'positive' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {exp.color === 'positive' ? '+' : ''}{exp.impact}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div className="card h-full flex items-center justify-center">
              <div className="text-center text-gray-400">
                <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <p className="text-sm">Fill in the parameters and run a prediction</p>
                <p className="text-xs mt-1">Results will appear here</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
