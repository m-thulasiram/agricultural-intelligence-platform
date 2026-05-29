import React, { useState, useRef } from 'react';
import { toast } from 'react-toastify';
import LineChart from '../components/charts/LineChart';
import BarChart from '../components/charts/BarChart';

export default function AdminPage() {
  const [activeSection, setActiveSection] = useState('data');
  const [uploading, setUploading] = useState(false);
  const [training, setTraining] = useState(false);
  const fileRef = useRef(null);

  const [modelVersions, setModelVersions] = useState([
    { version: 'v3.2.0', date: '2024-03-10', accuracy: 94.2, status: 'Active', size: '245 MB' },
    { version: 'v3.1.0', date: '2024-02-15', accuracy: 93.8, status: 'Archived', size: '240 MB' },
    { version: 'v3.0.0', date: '2024-01-20', accuracy: 92.5, status: 'Archived', size: '238 MB' },
    { version: 'v2.5.0', date: '2023-12-01', accuracy: 91.0, status: 'Archived', size: '220 MB' },
  ]);

  const [users] = useState([
    { id: 1, name: 'Admin User', email: 'admin@cropai.com', role: 'Admin', status: 'Active', lastActive: '2 min ago' },
    { id: 2, name: 'Farm Manager', email: 'manager@farm.com', role: 'Manager', status: 'Active', lastActive: '1h ago' },
    { id: 3, name: 'Analyst 1', email: 'analyst@cropai.com', role: 'Analyst', status: 'Active', lastActive: '3h ago' },
    { id: 4, name: 'Viewer User', email: 'viewer@cropai.com', role: 'Viewer', status: 'Inactive', lastActive: '2 days ago' },
  ]);

  const [systemHealth] = useState([
    { service: 'API Server', status: 'healthy', uptime: '99.98%', responseTime: '45ms' },
    { service: 'Database', status: 'healthy', uptime: '99.99%', responseTime: '12ms' },
    { service: 'ML Model Server', status: 'healthy', uptime: '99.95%', responseTime: '120ms' },
    { service: 'Cache Server', status: 'degraded', uptime: '98.50%', responseTime: '85ms' },
    { service: 'Storage Service', status: 'healthy', uptime: '99.97%', responseTime: '30ms' },
  ]);

  const [apiUsage] = useState([
    { month: 'Oct', predictions: 1250, forecasts: 340, recommendations: 890 },
    { month: 'Nov', predictions: 1480, forecasts: 420, recommendations: 1020 },
    { month: 'Dec', predictions: 1620, forecasts: 380, recommendations: 1150 },
    { month: 'Jan', predictions: 1890, forecasts: 520, recommendations: 1340 },
    { month: 'Feb', predictions: 2100, forecasts: 480, recommendations: 1480 },
    { month: 'Mar', predictions: 2350, forecasts: 560, recommendations: 1620 },
  ]);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    if (!file.name.endsWith('.csv')) {
      toast.error('Please upload a CSV file');
      return;
    }
    setUploading(true);
    await new Promise((r) => setTimeout(r, 2000));
    toast.success(`File "${file.name}" uploaded successfully!`);
    setUploading(false);
    if (fileRef.current) fileRef.current.value = '';
  };

  const handleTrainModel = async () => {
    setTraining(true);
    await new Promise((r) => setTimeout(r, 3000));
    const newVersion = `v3.${modelVersions.length}.0`;
    setModelVersions([
      { version: newVersion, date: new Date().toISOString().split('T')[0], accuracy: 94.0 + Math.random() * 1, status: 'Active', size: '248 MB' },
      ...modelVersions.map((m) => m.status === 'Active' ? { ...m, status: 'Archived' } : m),
    ]);
    toast.success(`Model ${newVersion} trained successfully!`);
    setTraining(false);
  };

  const sections = [
    { id: 'data', label: 'Data Management', icon: 'M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12' },
    { id: 'models', label: 'Model Management', icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
    { id: 'users', label: 'User Management', icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z' },
    { id: 'health', label: 'System Health', icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' },
    { id: 'api', label: 'API Usage', icon: 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Admin Panel</h1>
        <p className="text-sm text-gray-500 mt-1">System management and configuration</p>
      </div>

      <div className="flex gap-2 overflow-x-auto scrollbar-hide">
        {sections.map((s) => (
          <button
            key={s.id}
            onClick={() => setActiveSection(s.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
              activeSection === s.id
                ? 'bg-primary-600 text-white shadow-sm'
                : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
            }`}
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={s.icon} />
            </svg>
            {s.label}
          </button>
        ))}
      </div>

      {activeSection === 'data' && (
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Data Management</h2>
          <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-primary-400 transition-colors">
            <svg className="w-12 h-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p className="text-sm text-gray-600 mb-2">
              <span className="font-semibold">Click to upload</span> or drag and drop
            </p>
            <p className="text-xs text-gray-400 mb-4">CSV files only (max 50MB)</p>
            <input
              ref={fileRef}
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              className="hidden"
              id="csv-upload"
            />
            <label htmlFor="csv-upload" className="btn-primary cursor-pointer inline-flex">
              {uploading ? 'Uploading...' : 'Upload CSV'}
            </label>
          </div>
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-semibold text-gray-700 mb-2">Recent Uploads</h3>
            <div className="space-y-2">
              {['crop_data_2024.csv', 'soil_samples_march.csv', 'weather_forecast_q1.csv'].map((f, idx) => (
                <div key={idx} className="flex items-center justify-between text-sm py-1">
                  <div className="flex items-center gap-2">
                    <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span className="text-gray-600">{f}</span>
                  </div>
                  <span className="text-gray-400 text-xs">2 days ago</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeSection === 'models' && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Model Management</h2>
            <button onClick={handleTrainModel} disabled={training} className="btn-primary">
              {training ? (
                <span className="flex items-center gap-2">
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Training...
                </span>
              ) : 'Train New Model'}
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="table-header">Version</th>
                  <th className="table-header">Date</th>
                  <th className="table-header">Accuracy</th>
                  <th className="table-header">Status</th>
                  <th className="table-header">Size</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {modelVersions.map((m, idx) => (
                  <tr key={idx} className="hover:bg-gray-50">
                    <td className="table-cell font-mono font-medium">{m.version}</td>
                    <td className="table-cell">{m.date}</td>
                    <td className="table-cell">
                      <span className="font-medium text-green-600">{m.accuracy}%</span>
                    </td>
                    <td className="table-cell">
                      <span className={`badge ${m.status === 'Active' ? 'badge-green' : 'badge-yellow'}`}>
                        {m.status}
                      </span>
                    </td>
                    <td className="table-cell text-gray-500">{m.size}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeSection === 'users' && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">User Management</h2>
            <button className="btn-primary text-sm">Add User</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="table-header">Name</th>
                  <th className="table-header">Email</th>
                  <th className="table-header">Role</th>
                  <th className="table-header">Status</th>
                  <th className="table-header">Last Active</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-gray-50">
                    <td className="table-cell font-medium">{u.name}</td>
                    <td className="table-cell text-gray-500">{u.email}</td>
                    <td className="table-cell">
                      <span className={`badge ${
                        u.role === 'Admin' ? 'badge-red' : u.role === 'Manager' ? 'badge-blue' : u.role === 'Analyst' ? 'badge-yellow' : 'badge-green'
                      }`}>{u.role}</span>
                    </td>
                    <td className="table-cell">
                      <span className={`inline-flex items-center gap-1.5 text-sm ${
                        u.status === 'Active' ? 'text-green-600' : 'text-gray-400'
                      }`}>
                        <span className={`w-2 h-2 rounded-full ${u.status === 'Active' ? 'bg-green-500' : 'bg-gray-300'}`} />
                        {u.status}
                      </span>
                    </td>
                    <td className="table-cell text-gray-400">{u.lastActive}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeSection === 'health' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">System Health</h2>
            <div className="space-y-3">
              {systemHealth.map((s, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <span className={`w-2 h-2 rounded-full ${
                      s.status === 'healthy' ? 'bg-green-500' : 'bg-yellow-500'
                    }`} />
                    <span className="text-sm font-medium text-gray-700">{s.service}</span>
                  </div>
                  <div className="flex items-center gap-4 text-sm">
                    <span className="text-gray-500">{s.uptime}</span>
                    <span className="text-gray-400">{s.responseTime}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Performance Metrics</h2>
            <div className="grid grid-cols-2 gap-4">
              {[
                { label: 'Avg Response Time', value: '45ms', trend: '+12%', color: 'text-yellow-600' },
                { label: 'Requests/Min', value: '1,247', trend: '+8%', color: 'text-green-600' },
                { label: 'Error Rate', value: '0.02%', trend: '-5%', color: 'text-green-600' },
                { label: 'Memory Usage', value: '68%', trend: '+3%', color: 'text-yellow-600' },
              ].map((m, idx) => (
                <div key={idx} className="p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-500">{m.label}</p>
                  <p className="text-lg font-bold text-gray-900">{m.value}</p>
                  <span className={`text-xs font-medium ${m.color}`}>{m.trend}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeSection === 'api' && (
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">API Usage Statistics</h2>
          <BarChart
            data={apiUsage}
            bars={[
              { dataKey: 'predictions', name: 'Predictions' },
              { dataKey: 'forecasts', name: 'Forecasts' },
              { dataKey: 'recommendations', name: 'Recommendations' },
            ]}
            xKey="month"
            height={300}
            colors={['#22c55e', '#3b82f6', '#eab308']}
          />
          <div className="grid grid-cols-3 gap-4 mt-6 pt-4 border-t border-gray-100">
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-900">10,847</p>
              <p className="text-xs text-gray-500">Total API Calls</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">99.8%</p>
              <p className="text-xs text-gray-500">Success Rate</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-900">42ms</p>
              <p className="text-xs text-gray-500">Avg Latency</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
