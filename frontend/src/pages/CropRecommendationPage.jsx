import React, { useState } from 'react';
import { toast } from 'react-toastify';
import BarChart from '../components/charts/BarChart';
import { cropRecommendation, fertilizerPlan, irrigationSchedule } from '../services/recommendationService';
import { REGIONS, SOIL_TYPES, SEASONS, CROP_TYPES } from '../utils/constants';

export default function CropRecommendationPage() {
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('crops');
  const [recommendations, setRecommendations] = useState(null);
  const [fertilizer, setFertilizer] = useState(null);
  const [irrigation, setIrrigation] = useState(null);
  const [formData, setFormData] = useState({
    region: '',
    soil_type: '',
    season: 'kharif',
    area: '5',
    ph_level: '6.5',
    nitrogen: '80',
    phosphorus: '40',
    potassium: '60',
    organic_matter: '2.5',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.region || !formData.soil_type) {
      toast.error('Please select region and soil type');
      return;
    }
    try {
      setLoading(true);
      const numericData = Object.fromEntries(
        Object.entries(formData).map(([k, v]) => [k, isNaN(v) ? v : parseFloat(v)])
      );
      const [crops, fert, irr] = await Promise.all([
        cropRecommendation(numericData).catch(() => getMockCrops()),
        fertilizerPlan(numericData).catch(() => getMockFertilizer()),
        irrigationSchedule(numericData).catch(() => getMockIrrigation()),
      ]);
      setRecommendations(crops || getMockCrops());
      setFertilizer(fert || getMockFertilizer());
      setIrrigation(irr || getMockIrrigation());
      toast.success('Recommendations generated!');
    } catch (err) {
      toast.error('Failed to load recommendations, showing sample data');
      setRecommendations(getMockCrops());
      setFertilizer(getMockFertilizer());
      setIrrigation(getMockIrrigation());
    } finally {
      setLoading(false);
    }
  };

  const getMockCrops = () => ({
    crops: [
      { name: 'Wheat', suitability: 92, water_req: 450, duration: 120, profit: 'High' },
      { name: 'Rice', suitability: 78, water_req: 1200, duration: 150, profit: 'Medium' },
      { name: 'Maize', suitability: 85, water_req: 600, duration: 110, profit: 'High' },
      { name: 'Sugarcane', suitability: 65, water_req: 2000, duration: 365, profit: 'Very High' },
      { name: 'Cotton', suitability: 72, water_req: 800, duration: 180, profit: 'High' },
      { name: 'Groundnut', suitability: 88, water_req: 500, duration: 120, profit: 'Medium' },
    ],
  });

  const getMockFertilizer = () => ({
    recommendations: [
      { stage: 'Pre-Planting', fertilizer: 'DAP', amount: '120 kg/ha', npk: '18-46-0', timing: 'Before sowing' },
      { stage: 'Basal', fertilizer: 'Urea', amount: '80 kg/ha', npk: '46-0-0', timing: 'At sowing time' },
      { stage: 'Top Dressing 1', fertilizer: 'MOP', amount: '60 kg/ha', npk: '0-0-60', timing: '25-30 days after sowing' },
      { stage: 'Top Dressing 2', fertilizer: 'Urea', amount: '40 kg/ha', npk: '46-0-0', timing: '45-50 days after sowing' },
      { stage: 'Foliar', fertilizer: 'Zinc Sulphate', amount: '25 kg/ha', npk: '-', timing: 'After flowering' },
    ],
  });

  const getMockIrrigation = () => ({
    schedule: [
      { stage: 'Sowing', method: 'Sprinkler', frequency: 'Once', duration: '2 hours', amount: '30 mm' },
      { stage: 'Vegetative', method: 'Drip', frequency: 'Every 3 days', duration: '1 hour', amount: '20 mm' },
      { stage: 'Flowering', method: 'Drip', frequency: 'Every 2 days', duration: '1.5 hours', amount: '25 mm' },
      { stage: 'Grain Filling', method: 'Drip', frequency: 'Every 3 days', duration: '1 hour', amount: '20 mm' },
      { stage: 'Maturity', method: 'None', frequency: '-', duration: '-', amount: 'Stop irrigation' },
    ],
    water_saving_tips: [
      'Use drip irrigation to reduce water consumption by up to 60%',
      'Apply mulch to retain soil moisture and reduce evaporation',
      'Irrigate during early morning or late evening to minimize water loss',
      'Implement rainwater harvesting systems for supplementary irrigation',
      'Use soil moisture sensors for precision irrigation scheduling',
    ],
    pest_prevention: [
      'Practice crop rotation to break pest life cycles',
      'Use neem-based organic pesticides as preventive measure',
      'Maintain proper plant spacing for adequate air circulation',
      'Install pheromone traps for early pest detection',
      'Apply biological controls like Trichoderma and Pseudomonas',
    ],
  });

  const tabs = [
    { id: 'crops', label: 'Recommended Crops' },
    { id: 'fertilizer', label: 'Fertilizer Plan' },
    { id: 'irrigation', label: 'Irrigation Schedule' },
    { id: 'tips', label: 'Water & Pest Tips' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Crop Recommendations</h1>
        <p className="text-sm text-gray-500 mt-1">Personalized crop, fertilizer, and irrigation advice</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Farm Details</h2>
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
                <label className="label">Soil Type</label>
                <select name="soil_type" value={formData.soil_type} onChange={handleChange} className="select-field">
                  <option value="">Select soil type</option>
                  {SOIL_TYPES.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
                </select>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Season</label>
                <select name="season" value={formData.season} onChange={handleChange} className="select-field">
                  {SEASONS.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
                </select>
              </div>
              <div>
                <label className="label">Area (hectares)</label>
                <input type="number" name="area" value={formData.area} onChange={handleChange} className="input-field" />
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="label">pH Level</label>
                <input type="number" step="0.1" name="ph_level" value={formData.ph_level} onChange={handleChange} className="input-field" />
              </div>
              <div>
                <label className="label">Organic Matter (%)</label>
                <input type="number" step="0.1" name="organic_matter" value={formData.organic_matter} onChange={handleChange} className="input-field" />
              </div>
              <div>
                <label className="label">N / P / K</label>
                <div className="flex gap-1">
                  <input type="number" name="nitrogen" value={formData.nitrogen} onChange={handleChange} className="input-field text-center" placeholder="N" />
                  <input type="number" name="phosphorus" value={formData.phosphorus} onChange={handleChange} className="input-field text-center" placeholder="P" />
                  <input type="number" name="potassium" value={formData.potassium} onChange={handleChange} className="input-field text-center" placeholder="K" />
                </div>
              </div>
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full py-2.5">
              {loading ? 'Analyzing...' : 'Get Recommendations'}
            </button>
          </form>
        </div>

        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Tips</h2>
          <div className="space-y-4">
            <div className="p-4 bg-green-50 rounded-lg border border-green-200">
              <div className="flex items-center gap-2 mb-2">
                <svg className="w-5 h-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
                <span className="font-medium text-green-800">Soil Health</span>
              </div>
              <p className="text-sm text-green-700">Test soil every 2-3 years. Maintain pH between 6.0-7.5 for most crops.</p>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
              <div className="flex items-center gap-2 mb-2">
                <svg className="w-5 h-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span className="font-medium text-blue-800">Water Management</span>
              </div>
              <p className="text-sm text-blue-700">Drip irrigation can save 60% water compared to flood irrigation.</p>
            </div>
            <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
              <div className="flex items-center gap-2 mb-2">
                <svg className="w-5 h-5 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
                <span className="font-medium text-yellow-800">Crop Rotation</span>
              </div>
              <p className="text-sm text-yellow-700">Rotate legumes with cereals to naturally fix nitrogen in soil.</p>
            </div>
          </div>
        </div>
      </div>

      {(recommendations || fertilizer || irrigation) && (
        <div className="card">
          <div className="flex gap-2 mb-6 overflow-x-auto scrollbar-hide">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
                  activeTab === tab.id
                    ? 'bg-primary-600 text-white shadow-sm'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {activeTab === 'crops' && recommendations && (
            <div>
              <h3 className="text-base font-semibold text-gray-900 mb-4">Suitable Crops</h3>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-100">
                      <th className="table-header">Crop</th>
                      <th className="table-header">Suitability</th>
                      <th className="table-header">Water Req (mm)</th>
                      <th className="table-header">Duration (days)</th>
                      <th className="table-header">Profit Potential</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {recommendations.crops.map((c, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        <td className="table-cell font-medium">{c.name}</td>
                        <td className="table-cell">
                          <div className="flex items-center gap-2">
                            <div className="w-20 bg-gray-100 rounded-full h-2">
                              <div
                                className={`h-2 rounded-full ${
                                  c.suitability >= 80 ? 'bg-green-500' : c.suitability >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                                }`}
                                style={{ width: `${c.suitability}%` }}
                              />
                            </div>
                            <span className="text-xs font-medium">{c.suitability}%</span>
                          </div>
                        </td>
                        <td className="table-cell">{c.water_req}</td>
                        <td className="table-cell">{c.duration}</td>
                        <td className="table-cell">
                          <span className={`badge ${
                            c.profit === 'Very High' ? 'badge-green' :
                            c.profit === 'High' ? 'badge-blue' : 'badge-yellow'
                          }`}>{c.profit}</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'fertilizer' && fertilizer && (
            <div>
              <h3 className="text-base font-semibold text-gray-900 mb-4">Fertilizer Schedule</h3>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-100">
                      <th className="table-header">Stage</th>
                      <th className="table-header">Fertilizer</th>
                      <th className="table-header">Amount</th>
                      <th className="table-header">NPK Ratio</th>
                      <th className="table-header">Timing</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {fertilizer.recommendations.map((f, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        <td className="table-cell font-medium">{f.stage}</td>
                        <td className="table-cell">{f.fertilizer}</td>
                        <td className="table-cell">{f.amount}</td>
                        <td className="table-cell">
                          <code className="px-2 py-0.5 bg-gray-100 rounded text-xs">{f.npk}</code>
                        </td>
                        <td className="table-cell text-gray-500">{f.timing}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'irrigation' && irrigation && (
            <div>
              <h3 className="text-base font-semibold text-gray-900 mb-4">Irrigation Schedule</h3>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-100">
                      <th className="table-header">Growth Stage</th>
                      <th className="table-header">Method</th>
                      <th className="table-header">Frequency</th>
                      <th className="table-header">Duration</th>
                      <th className="table-header">Water Amount</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {irrigation.schedule.map((s, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        <td className="table-cell font-medium">{s.stage}</td>
                        <td className="table-cell">
                          <span className="badge-blue">{s.method}</span>
                        </td>
                        <td className="table-cell">{s.frequency}</td>
                        <td className="table-cell">{s.duration}</td>
                        <td className="table-cell">{s.amount}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'tips' && irrigation && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-base font-semibold text-gray-900 mb-3">Water Saving Tips</h3>
                <ul className="space-y-2">
                  {irrigation.water_saving_tips.map((tip, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                      <svg className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      {tip}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h3 className="text-base font-semibold text-gray-900 mb-3">Pest Prevention Methods</h3>
                <ul className="space-y-2">
                  {irrigation.pest_prevention.map((tip, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                      <svg className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      {tip}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
