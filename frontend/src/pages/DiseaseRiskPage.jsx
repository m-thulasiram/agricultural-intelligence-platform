import React, { useState } from 'react';
import { toast } from 'react-toastify';
import HealthGauge from '../components/dashboard/HealthGauge';
import BarChart from '../components/charts/BarChart';
import PieChart from '../components/charts/PieChart';
import { diseaseRisk } from '../services/diseaseService';
import { REGIONS, CROP_TYPES, SEASONS } from '../utils/constants';

export default function DiseaseRiskPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [formData, setFormData] = useState({
    region: '',
    crop_type: '',
    season: 'kharif',
    year: '2024',
    humidity: '65',
    temperature: '28',
    rainfall: '850',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.region || !formData.crop_type) {
      toast.error('Please select region and crop type');
      return;
    }
    try {
      setLoading(true);
      const numericData = Object.fromEntries(
        Object.entries(formData).map(([k, v]) => [k, isNaN(v) ? v : parseFloat(v)])
      );
      const data = await diseaseRisk(numericData);
      setResult(data);
      toast.success('Risk analysis completed!');
    } catch (err) {
      toast.error(err.message || 'Analysis failed, showing sample data');
      setResult(getMockResult());
    } finally {
      setLoading(false);
    }
  };

  const getMockResult = () => ({
    pest_attack_prob: 15 + Math.random() * 60,
    disease_outbreak_prob: 10 + Math.random() * 50,
    seasonal_risk: [
      { season: 'Winter', risk: 20 },
      { season: 'Spring', risk: 35 },
      { season: 'Summer', risk: 65 },
      { season: 'Monsoon', risk: 80 },
      { season: 'Autumn', risk: 45 },
    ],
    disease_types: [
      { name: 'Fungal', value: 35 },
      { name: 'Bacterial', value: 25 },
      { name: 'Viral', value: 20 },
      { name: 'Pest', value: 15 },
      { name: 'Nutritional', value: 5 },
    ],
    preventive_measures: [
      'Apply copper-based fungicides before monsoon season',
      'Maintain proper drainage to prevent fungal growth',
      'Use disease-resistant seed varieties',
      'Practice 3-year crop rotation cycles',
      'Install yellow sticky traps for pest monitoring',
      'Apply neem oil spray every 15 days during high-risk season',
      'Ensure adequate spacing between plants for air circulation',
    ],
    regional_hotspots: [
      { region: 'Delta Region', risk: 78 },
      { region: 'Coastal Belt', risk: 65 },
      { region: 'Plateau Area', risk: 45 },
      { region: 'Valley Zone', risk: 55 },
    ],
  });

  const m = result || getMockResult();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Disease & Pest Risk Analysis</h1>
        <p className="text-sm text-gray-500 mt-1">Assess disease and pest outbreak probabilities</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Risk Assessment Inputs</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Region</label>
                <select name="region" value={formData.region} onChange={handleChange} className="select-field">
                  <option value="">Select region</option>
                  {REGIONS.map((r) => <option key={r.value} value={r.value}>{r.label}</option>)}
                </select>
              </div>
              <div>
                <label className="label">Crop Type</label>
                <select name="crop_type" value={formData.crop_type} onChange={handleChange} className="select-field">
                  <option value="">Select crop</option>
                  {CROP_TYPES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
                </select>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="label">Season</label>
                <select name="season" value={formData.season} onChange={handleChange} className="select-field">
                  {SEASONS.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
                </select>
              </div>
              <div>
                <label className="label">Year</label>
                <input type="number" name="year" value={formData.year} onChange={handleChange} className="input-field" />
              </div>
              <div>
                <label className="label">Humidity (%)</label>
                <input type="number" name="humidity" value={formData.humidity} onChange={handleChange} className="input-field" />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Temperature (°C)</label>
                <input type="number" step="0.1" name="temperature" value={formData.temperature} onChange={handleChange} className="input-field" />
              </div>
              <div>
                <label className="label">Rainfall (mm)</label>
                <input type="number" step="0.1" name="rainfall" value={formData.rainfall} onChange={handleChange} className="input-field" />
              </div>
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full py-2.5">
              {loading ? 'Analyzing...' : 'Analyze Risk'}
            </button>
          </form>
        </div>

        <div className="space-y-6">
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Risk Probabilities</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-500 mb-2">Pest Attack</p>
                <div className="relative w-24 h-24 mx-auto">
                  <svg className="w-24 h-24 -rotate-90" viewBox="0 0 36 36">
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e5e7eb" strokeWidth="4" />
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke={m.pest_attack_prob > 50 ? '#ef4444' : m.pest_attack_prob > 30 ? '#eab308' : '#22c55e'} strokeWidth="4" strokeDasharray={`${m.pest_attack_prob}, 100`} />
                  </svg>
                  <span className="absolute inset-0 flex items-center justify-center text-lg font-bold text-gray-900">
                    {Math.round(m.pest_attack_prob)}%
                  </span>
                </div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-500 mb-2">Disease Outbreak</p>
                <div className="relative w-24 h-24 mx-auto">
                  <svg className="w-24 h-24 -rotate-90" viewBox="0 0 36 36">
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e5e7eb" strokeWidth="4" />
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke={m.disease_outbreak_prob > 50 ? '#ef4444' : m.disease_outbreak_prob > 30 ? '#eab308' : '#22c55e'} strokeWidth="4" strokeDasharray={`${m.disease_outbreak_prob}, 100`} />
                  </svg>
                  <span className="absolute inset-0 flex items-center justify-center text-lg font-bold text-gray-900">
                    {Math.round(m.disease_outbreak_prob)}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Seasonal Risk</h2>
          <BarChart
            data={m.seasonal_risk}
            bars={[{ dataKey: 'risk', name: 'Risk Level' }]}
            xKey="season"
            height={250}
            colors={['#ef4444']}
          />
        </div>
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Disease Distribution</h2>
          <PieChart
            data={m.disease_types}
            dataKey="value"
            nameKey="name"
            height={250}
            innerRadius={50}
            outerRadius={90}
            colors={['#ef4444', '#f97316', '#eab308', '#22c55e', '#6366f1']}
          />
        </div>
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Regional Hotspots</h2>
          <div className="space-y-4">
            {m.regional_hotspots.map((h, idx) => (
              <div key={idx}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">{h.region}</span>
                  <span className={`font-medium ${
                    h.risk >= 70 ? 'text-red-600' : h.risk >= 50 ? 'text-yellow-600' : 'text-green-600'
                  }`}>{h.risk}%</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      h.risk >= 70 ? 'bg-red-500' : h.risk >= 50 ? 'bg-yellow-500' : 'bg-green-500'
                    }`}
                    style={{ width: `${h.risk}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Preventive Measures</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {m.preventive_measures.map((measure, idx) => (
            <div key={idx} className="flex items-start gap-2 p-3 bg-gray-50 rounded-lg hover:bg-green-50 transition-colors">
              <svg className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              <span className="text-sm text-gray-700">{measure}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
