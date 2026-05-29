import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import StatCard from '../components/dashboard/StatCard';
import HealthGauge from '../components/dashboard/HealthGauge';
import AreaChart from '../components/charts/AreaChart';
import BarChart from '../components/charts/BarChart';
import { getDashboardSummary } from '../services/analyticsService';
import { MONTHS } from '../utils/constants';

export default function HomePage() {
  const [loading, setLoading] = useState(true);
  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const isValidDashboardData = (data) => {
    return data && data.stats && data.healthOverview && data.recentPredictions;
  };

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const data = await getDashboardSummary();
      if (isValidDashboardData(data)) {
        setDashboard(data);
      } else {
        setDashboard(getMockDashboardData());
      }
    } catch (err) {
      toast.error('Failed to load dashboard data');
      setDashboard(getMockDashboardData());
    } finally {
      setLoading(false);
    }
  };

  const getMockDashboardData = () => ({
    stats: {
      totalPredictions: 12847,
      activeRegions: 24,
      avgHealthIndex: 72.5,
      riskAlerts: 8,
    },
    healthOverview: MONTHS.map((m) => ({
      name: m,
      health: 50 + Math.random() * 40,
      rainfall: 20 + Math.random() * 80,
      temperature: 15 + Math.random() * 20,
    })),
    recentPredictions: [
      { id: 1, region: 'North India', crop: 'Wheat', healthIndex: 85, risk: 'Low', date: '2024-03-15' },
      { id: 2, region: 'South India', crop: 'Rice', healthIndex: 62, risk: 'Moderate', date: '2024-03-14' },
      { id: 3, region: 'East India', crop: 'Sugarcane', healthIndex: 45, risk: 'High', date: '2024-03-14' },
      { id: 4, region: 'West India', crop: 'Cotton', healthIndex: 78, risk: 'Low', date: '2024-03-13' },
      { id: 5, region: 'Central India', crop: 'Maize', healthIndex: 55, risk: 'Moderate', date: '2024-03-13' },
    ],
    climateTrend: [
      { year: '2020', avg: 24.5, min: 18.2, max: 31.8 },
      { year: '2021', avg: 25.1, min: 19.0, max: 32.5 },
      { year: '2022', avg: 24.8, min: 18.5, max: 32.0 },
      { year: '2023', avg: 25.6, min: 19.3, max: 33.1 },
      { year: '2024', avg: 26.2, min: 20.1, max: 33.8 },
    ],
    cropDistribution: [
      { name: 'Wheat', value: 28 },
      { name: 'Rice', value: 24 },
      { name: 'Maize', value: 18 },
      { name: 'Sugarcane', value: 15 },
      { name: 'Cotton', value: 10 },
      { name: 'Others', value: 5 },
    ],
    alerts: [
      { type: 'warning', message: 'Drought risk increasing in Central India', time: '2h ago' },
      { type: 'info', message: 'Optimal planting window for Rabi crops approaching', time: '5h ago' },
      { type: 'success', message: 'North India soil moisture levels are healthy', time: '1d ago' },
      { type: 'error', message: 'Pest outbreak reported in East India rice fields', time: '2d ago' },
    ],
  });

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => <StatCard key={i} loading />)}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 card h-80 animate-pulse">
            <div className="h-full bg-gray-200 rounded" />
          </div>
          <div className="card h-80 animate-pulse">
            <div className="h-full bg-gray-200 rounded" />
          </div>
        </div>
      </div>
    );
  }

  const d = dashboard || getMockDashboardData();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">Your agricultural intelligence overview</p>
        </div>
        <div className="flex gap-2">
          <button onClick={fetchDashboard} className="btn-secondary text-sm">
            <svg className="w-4 h-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
          label="Total Predictions"
          value={d.stats.totalPredictions.toLocaleString()}
          trend={12}
          color="primary"
        />
        <StatCard
          icon="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z M15 11a3 3 0 11-6 0 3 3 0 016 0z"
          label="Active Regions"
          value={d.stats.activeRegions}
          trend={0}
          color="blue"
        />
        <StatCard
          icon="M13 10V3L4 14h7v7l9-11h-7z"
          label="Avg Health Index"
          value={`${d.stats.avgHealthIndex}%`}
          trend={5}
          color="green"
        />
        <StatCard
          icon="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"
          label="Risk Alerts"
          value={d.stats.riskAlerts}
          trend={-3}
          color="red"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Crop Health Overview</h2>
            <Link to="/climate-analysis" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
              View Details →
            </Link>
          </div>
          <AreaChart
            data={d.healthOverview}
            areas={[
              { dataKey: 'health', name: 'Health Index' },
              { dataKey: 'rainfall', name: 'Rainfall (mm)' },
            ]}
            height={280}
          />
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Health Index</h2>
          </div>
          <div className="flex flex-col items-center py-4">
            <HealthGauge value={d.stats.avgHealthIndex} size="lg" />
          </div>
          <div className="space-y-3 mt-4 pt-4 border-t border-gray-100">
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">Crop Distribution</span>
            </div>
            {d.cropDistribution.slice(0, 4).map((crop) => (
              <div key={crop.name} className="flex items-center justify-between text-sm">
                <span className="text-gray-600">{crop.name}</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-gray-100 rounded-full h-2">
                    <div
                      className="bg-primary-500 h-2 rounded-full transition-all"
                      style={{ width: `${crop.value}%` }}
                    />
                  </div>
                  <span className="text-gray-900 font-medium w-8 text-right">{crop.value}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Recent Predictions</h2>
            <Link to="/predict" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
              New Prediction →
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="table-header">Region</th>
                  <th className="table-header">Crop</th>
                  <th className="table-header">Health</th>
                  <th className="table-header">Risk</th>
                  <th className="table-header">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {d.recentPredictions.map((p) => (
                  <tr key={p.id} className="hover:bg-gray-50 transition-colors">
                    <td className="table-cell font-medium">{p.region}</td>
                    <td className="table-cell">{p.crop}</td>
                    <td className="table-cell">
                      <span className={`inline-flex items-center gap-1.5 ${
                        p.healthIndex >= 70 ? 'text-green-600' : p.healthIndex >= 50 ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        <span className={`w-2 h-2 rounded-full ${
                          p.healthIndex >= 70 ? 'bg-green-500' : p.healthIndex >= 50 ? 'bg-yellow-500' : 'bg-red-500'
                        }`} />
                        {p.healthIndex}%
                      </span>
                    </td>
                    <td className="table-cell">
                      <span className={`badge ${
                        p.risk === 'Low' ? 'badge-green' : p.risk === 'Moderate' ? 'badge-yellow' : 'badge-red'
                      }`}>
                        {p.risk}
                      </span>
                    </td>
                    <td className="table-cell text-gray-400">{p.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Climate Trend</h2>
            <span className="text-xs text-gray-400">Temperature °C</span>
          </div>
          <BarChart
            data={d.climateTrend}
            bars={[
              { dataKey: 'avg', name: 'Avg Temp' },
              { dataKey: 'min', name: 'Min Temp' },
              { dataKey: 'max', name: 'Max Temp' },
            ]}
            xKey="year"
            height={280}
          />
        </div>
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Alerts</h2>
        <div className="space-y-3">
          {d.alerts.map((alert, idx) => (
            <div key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors">
              <div className={`p-1.5 rounded-full ${
                alert.type === 'error' ? 'bg-red-100 text-red-600' :
                alert.type === 'warning' ? 'bg-yellow-100 text-yellow-600' :
                alert.type === 'success' ? 'bg-green-100 text-green-600' :
                'bg-blue-100 text-blue-600'
              }`}>
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  {alert.type === 'error' ? (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  ) : alert.type === 'warning' ? (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  ) : alert.type === 'success' ? (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  ) : (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  )}
                </svg>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-800">{alert.message}</p>
                <p className="text-xs text-gray-400 mt-0.5">{alert.time}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
