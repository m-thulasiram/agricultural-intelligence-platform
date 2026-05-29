import React, { useState } from 'react';
import { toast } from 'react-toastify';
import HealthGauge from '../components/dashboard/HealthGauge';
import LineChart from '../components/charts/LineChart';
import AreaChart from '../components/charts/AreaChart';
import BarChart from '../components/charts/BarChart';
import { futureForecast, compareModels } from '../services/forecastService';
import { REGIONS } from '../utils/constants';

export default function ForecastPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [modelComparison, setModelComparison] = useState(null);
  const [formData, setFormData] = useState({
    region: '',
    forecastYears: 10,
    includeExtremes: true,
  });
  const [showCustom, setShowCustom] = useState(false);

  const forecastOptions = [
    { value: 5, label: '5 Years' },
    { value: 10, label: '10 Years' },
    { value: 20, label: '20 Years' },
    { value: 50, label: '50 Years' },
    { value: 'custom', label: 'Custom' },
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.region) {
      toast.error('Please select a region');
      return;
    }
    try {
      setLoading(true);
      const data = await futureForecast({
        region: formData.region,
        years: formData.forecastYears,
        include_extremes: formData.includeExtremes,
      });
      setResult(data);
      toast.success('Forecast generated successfully!');
    } catch (err) {
      toast.error(err.message || 'Failed to generate forecast');
      setResult(getMockForecast());
    } finally {
      setLoading(false);
    }
  };

  const loadModelComparison = async () => {
    try {
      const data = await compareModels();
      setModelComparison(data);
    } catch {
      setModelComparison(getMockModelComparison());
    }
  };

  const getMockForecast = () => {
    const years = formData.forecastYears === 'custom' ? 15 : formData.forecastYears;
    const data = [];
    for (let i = 0; i <= years; i++) {
      const year = 2024 + i;
      data.push({
        year: year.toString(),
        rainfall: 700 + Math.sin(i * 0.5) * 200 + Math.random() * 100,
        temp: 25 + Math.sin(i * 0.3) * 3 + Math.random() * 2,
        droughtProb: Math.max(0, Math.min(100, 20 + Math.sin(i * 0.7) * 15 + Math.random() * 10)),
        floodProb: Math.max(0, Math.min(100, 15 + Math.cos(i * 0.4) * 12 + Math.random() * 8)),
      });
    }
    return {
      forecast: data,
      climate_impact_score: 55 + Math.random() * 30,
      summary: {
        avg_temp_change: '+1.8°C',
        rainfall_variability: '±15%',
        extreme_events: 'Increased likelihood of droughts in central regions',
      },
    };
  };

  const getMockModelComparison = () => ({
    models: [
      { name: 'Random Forest', mae: 0.32, rmse: 0.45, r2: 0.89, training_time: 45 },
      { name: 'XGBoost', mae: 0.28, rmse: 0.41, r2: 0.92, training_time: 62 },
      { name: 'LSTM', mae: 0.35, rmse: 0.48, r2: 0.87, training_time: 180 },
      { name: 'Linear Regression', mae: 0.52, rmse: 0.68, r2: 0.72, training_time: 12 },
      { name: 'Gradient Boost', mae: 0.30, rmse: 0.43, r2: 0.90, training_time: 55 },
    ],
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Climate Forecast</h1>
        <p className="text-sm text-gray-500 mt-1">Long-term climate projections and impact analysis</p>
      </div>

      <div className="card">
        <form onSubmit={handleSubmit} className="flex flex-wrap items-end gap-4">
          <div className="w-full sm:w-48">
            <label className="label">Region</label>
            <select
              value={formData.region}
              onChange={(e) => setFormData({ ...formData, region: e.target.value })}
              className="select-field"
            >
              <option value="">Select region</option>
              {REGIONS.map((r) => <option key={r.value} value={r.value}>{r.label}</option>)}
            </select>
          </div>
          <div className="w-full sm:w-40">
            <label className="label">Forecast Period</label>
            <select
              value={formData.forecastYears}
              onChange={(e) => {
                const val = e.target.value;
                setShowCustom(val === 'custom');
                setFormData({ ...formData, forecastYears: val === 'custom' ? 15 : parseInt(val) });
              }}
              className="select-field"
            >
              {forecastOptions.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          </div>
          {showCustom && (
            <div className="w-full sm:w-32">
              <label className="label">Years</label>
              <input
                type="number"
                min={1}
                max={100}
                value={formData.forecastYears}
                onChange={(e) => setFormData({ ...formData, forecastYears: parseInt(e.target.value) || 1 })}
                className="input-field"
              />
            </div>
          )}
          <div className="flex items-center gap-2 pb-1">
            <input
              type="checkbox"
              id="extremes"
              checked={formData.includeExtremes}
              onChange={(e) => setFormData({ ...formData, includeExtremes: e.target.checked })}
              className="w-4 h-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            <label htmlFor="extremes" className="text-sm text-gray-600">Include Extremes</label>
          </div>
          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Generating...' : 'Generate Forecast'}
          </button>
        </form>
      </div>

      {result && (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="card lg:col-span-2">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Rainfall & Temperature Forecast</h2>
              <LineChart
                data={result.forecast}
                lines={[
                  { dataKey: 'rainfall', name: 'Rainfall (mm)' },
                  { dataKey: 'temp', name: 'Temperature (°C)' },
                ]}
                xKey="year"
                height={300}
              />
            </div>
            <div className="card flex flex-col items-center justify-center">
              <h2 className="text-lg font-semibold text-gray-900 mb-2">Climate Impact Score</h2>
              <HealthGauge value={result.climate_impact_score} size="lg" label="Resilience Score" />
              <div className="mt-4 space-y-2 w-full">
                {Object.entries(result.summary).map(([key, val]) => (
                  <div key={key} className="flex justify-between text-sm px-3 py-1.5 bg-gray-50 rounded-lg">
                    <span className="text-gray-500 capitalize">{key.replace(/_/g, ' ')}</span>
                    <span className="font-medium text-gray-800">{val}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Drought Probability</h2>
              <AreaChart
                data={result.forecast}
                areas={[{ dataKey: 'droughtProb', name: 'Drought Probability %' }]}
                xKey="year"
                height={250}
                colors={['#f97316']}
              />
            </div>
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Flood Probability</h2>
              <AreaChart
                data={result.forecast}
                areas={[{ dataKey: 'floodProb', name: 'Flood Probability %' }]}
                xKey="year"
                height={250}
                colors={['#3b82f6']}
              />
            </div>
          </div>
        </>
      )}

      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Model Comparison</h2>
          <button onClick={loadModelComparison} className="btn-secondary text-sm">
            Load Comparison
          </button>
        </div>
        {modelComparison ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="table-header">Model</th>
                  <th className="table-header">MAE</th>
                  <th className="table-header">RMSE</th>
                  <th className="table-header">R² Score</th>
                  <th className="table-header">Training Time (s)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {modelComparison.models.map((m, idx) => (
                  <tr key={idx} className="hover:bg-gray-50">
                    <td className="table-cell font-medium">{m.name}</td>
                    <td className="table-cell">{m.mae.toFixed(3)}</td>
                    <td className="table-cell">{m.rmse.toFixed(3)}</td>
                    <td className="table-cell">
                      <span className={`font-medium ${m.r2 >= 0.85 ? 'text-green-600' : m.r2 >= 0.75 ? 'text-yellow-600' : 'text-red-600'}`}>
                        {m.r2.toFixed(3)}
                      </span>
                    </td>
                    <td className="table-cell">{m.training_time}s</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-sm text-gray-400 text-center py-8">Click to load model comparison data</p>
        )}
      </div>
    </div>
  );
}
