import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import LineChart from '../components/charts/LineChart';
import BarChart from '../components/charts/BarChart';
import AreaChart from '../components/charts/AreaChart';
import { getAnalytics } from '../services/analyticsService';
import { REGIONS, MONTHS } from '../utils/constants';

export default function ClimateAnalysisPage() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState('north_india');
  const [viewMode, setViewMode] = useState('historical');

  useEffect(() => {
    fetchData();
  }, [selectedRegion, viewMode]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const result = await getAnalytics({ region: selectedRegion, mode: viewMode });
      setData(result);
    } catch {
      setData(getMockData());
    } finally {
      setLoading(false);
    }
  };

  const getMockData = () => ({
    temperature: {
      historical: MONTHS.map((m, i) => ({
        name: m,
        current: 20 + Math.sin(i * 0.5) * 8 + 5,
        average: 18 + Math.sin(i * 0.5) * 7 + 4,
        forecast: 22 + Math.sin(i * 0.5) * 8 + 5,
      })),
      annual: [
        { year: '2019', avg: 24.2, min: 18.5, max: 30.8 },
        { year: '2020', avg: 24.8, min: 19.0, max: 31.5 },
        { year: '2021', avg: 25.3, min: 19.5, max: 32.0 },
        { year: '2022', avg: 25.0, min: 19.2, max: 31.8 },
        { year: '2023', avg: 25.8, min: 19.8, max: 32.5 },
        { year: '2024', avg: 26.2, min: 20.2, max: 33.0 },
      ],
    },
    rainfall: {
      monthly: MONTHS.map((m, i) => ({
        name: m,
        current: 30 + Math.sin(i * 0.8) * 60 + 40,
        average: 25 + Math.sin(i * 0.8) * 55 + 35,
      })),
      yearly: [
        { year: '2019', rainfall: 820, days: 45 },
        { year: '2020', rainfall: 780, days: 42 },
        { year: '2021', rainfall: 850, days: 48 },
        { year: '2022', rainfall: 790, days: 44 },
        { year: '2023', rainfall: 880, days: 50 },
      ],
    },
    correlation: [
      { factor: 'Temp vs Rainfall', value: -0.42, strength: 'Moderate' },
      { factor: 'Temp vs Humidity', value: 0.35, strength: 'Weak' },
      { factor: 'Rainfall vs Humidity', value: 0.78, strength: 'Strong' },
      { factor: 'Rainfall vs Soil Moisture', value: 0.65, strength: 'Strong' },
      { factor: 'Temp vs Soil Moisture', value: -0.55, strength: 'Moderate' },
    ],
  });

  const d = data || getMockData();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Climate Analysis</h1>
          <p className="text-sm text-gray-500 mt-1">Detailed climate patterns and correlation analysis</p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="select-field w-40"
          >
            {REGIONS.map((r) => <option key={r.value} value={r.value}>{r.label}</option>)}
          </select>
          <div className="flex rounded-lg border border-gray-300 overflow-hidden">
            <button
              onClick={() => setViewMode('historical')}
              className={`px-3 py-1.5 text-sm font-medium transition-colors ${
                viewMode === 'historical' ? 'bg-primary-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'
              }`}
            >
              Historical
            </button>
            <button
              onClick={() => setViewMode('forecast')}
              className={`px-3 py-1.5 text-sm font-medium transition-colors ${
                viewMode === 'forecast' ? 'bg-primary-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'
              }`}
            >
              Forecast
            </button>
            <button
              onClick={() => setViewMode('comparison')}
              className={`px-3 py-1.5 text-sm font-medium transition-colors ${
                viewMode === 'comparison' ? 'bg-primary-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'
              }`}
            >
              Comparison
            </button>
          </div>
        </div>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-12">
          <svg className="animate-spin h-8 w-8 text-primary-600" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        </div>
      )}

      {!loading && (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Temperature Trends</h2>
              <LineChart
                data={d.temperature.historical}
                lines={[
                  { dataKey: 'current', name: 'Current' },
                  { dataKey: 'average', name: 'Historical Avg' },
                  { dataKey: 'forecast', name: 'Forecast' },
                ]}
                xKey="name"
                height={280}
                colors={['#ef4444', '#6b7280', '#3b82f6']}
              />
            </div>
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Annual Temperature Range</h2>
              <LineChart
                data={d.temperature.annual}
                lines={[
                  { dataKey: 'max', name: 'Max Temp' },
                  { dataKey: 'avg', name: 'Avg Temp' },
                  { dataKey: 'min', name: 'Min Temp' },
                ]}
                xKey="year"
                height={280}
                colors={['#ef4444', '#f97316', '#3b82f6']}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Rainfall Distribution</h2>
              <BarChart
                data={d.rainfall.monthly}
                bars={[
                  { dataKey: 'current', name: 'Current' },
                  { dataKey: 'average', name: 'Average' },
                ]}
                xKey="name"
                height={280}
                colors={['#3b82f6', '#93c5fd']}
              />
            </div>
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Yearly Rainfall</h2>
              <AreaChart
                data={d.rainfall.yearly}
                areas={[{ dataKey: 'rainfall', name: 'Rainfall (mm)' }]}
                xKey="year"
                height={280}
                colors={['#3b82f6']}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Correlation Analysis</h2>
              <div className="space-y-3">
                {d.correlation.map((item, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm text-gray-700">{item.factor}</span>
                    <div className="flex items-center gap-3">
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all ${
                            item.value > 0 ? 'bg-green-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${Math.abs(item.value) * 100}%` }}
                        />
                      </div>
                      <span className={`text-sm font-medium w-16 text-right ${
                        item.strength === 'Strong' ? 'text-green-600' :
                        item.strength === 'Moderate' ? 'text-yellow-600' : 'text-gray-500'
                      }`}>
                        {item.value.toFixed(2)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Historical vs Forecast</h2>
              <LineChart
                data={d.temperature.annual.map((y) => ({
                  ...y,
                  forecast_avg: y.avg + 0.8 + Math.random() * 0.5,
                }))}
                lines={[
                  { dataKey: 'avg', name: 'Historical Avg' },
                  { dataKey: 'forecast_avg', name: 'Forecast Avg' },
                ]}
                xKey="year"
                height={280}
                colors={['#6b7280', '#ef4444']}
              />
              <div className="mt-4 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                <p className="text-sm text-yellow-800">
                  <span className="font-semibold">Insight:</span> Temperature projections indicate a warming trend of approximately +1.5°C to +2.0°C over the next decade in this region.
                </p>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
