import React, { useState } from 'react';
import { toast } from 'react-toastify';
import { saveAs } from 'file-saver';
import { format } from 'date-fns';
import { REGIONS, CROP_TYPES } from '../utils/constants';

export default function ReportsPage() {
  const [loading, setLoading] = useState(false);
  const [generated, setGenerated] = useState(false);
  const [formData, setFormData] = useState({
    reportType: 'crop_health',
    region: '',
    crop: '',
    startDate: format(new Date(new Date().setMonth(new Date().getMonth() - 3)), 'yyyy-MM-dd'),
    endDate: format(new Date(), 'yyyy-MM-dd'),
    format: 'pdf',
  });

  const [reportHistory] = useState([
    { id: 1, name: 'North India Crop Health Report', type: 'Crop Health', date: '2024-03-10', status: 'Ready', size: '2.4 MB' },
    { id: 2, name: 'Q1 Climate Analysis 2024', type: 'Climate', date: '2024-03-01', status: 'Ready', size: '4.1 MB' },
    { id: 3, name: 'Fertilizer Recommendation - Wheat', type: 'Fertilizer', date: '2024-02-25', status: 'Ready', size: '1.2 MB' },
    { id: 4, name: 'Disease Risk Assessment - Rice', type: 'Disease Risk', date: '2024-02-20', status: 'Generating', size: '-' },
    { id: 5, name: 'Annual Yield Report 2023', type: 'Yield', date: '2023-12-31', status: 'Ready', size: '5.8 MB' },
    { id: 6, name: 'Soil Analysis - Central India', type: 'Soil', date: '2023-12-15', status: 'Ready', size: '3.2 MB' },
  ]);

  const reportTypes = [
    { value: 'crop_health', label: 'Crop Health Report' },
    { value: 'climate', label: 'Climate Analysis Report' },
    { value: 'fertilizer', label: 'Fertilizer Recommendation' },
    { value: 'disease_risk', label: 'Disease Risk Assessment' },
    { value: 'yield', label: 'Yield Prediction Report' },
    { value: 'soil', label: 'Soil Analysis Report' },
  ];

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!formData.region) {
      toast.error('Please select a region');
      return;
    }
    try {
      setLoading(true);
      await new Promise((r) => setTimeout(r, 2500));
      setGenerated(true);
      toast.success('Report generated successfully!');
    } catch {
      toast.error('Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (reportName) => {
    try {
      const blob = new Blob(['Sample report content'], { type: 'application/pdf' });
      saveAs(blob, `${reportName || 'report'}.pdf`);
      toast.success('Download started');
    } catch {
      toast.error('Download failed');
    }
  };

  const getStatusIcon = (status) => {
    if (status === 'Ready') {
      return (
        <svg className="w-5 h-5 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      );
    }
    return (
      <svg className="w-5 h-5 text-yellow-500 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Reports</h1>
        <p className="text-sm text-gray-500 mt-1">Generate and download agricultural reports</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Generate Report</h2>
          <form onSubmit={handleGenerate} className="space-y-4">
            <div>
              <label className="label">Report Type</label>
              <select name="reportType" value={formData.reportType} onChange={handleChange} className="select-field">
                {reportTypes.map((r) => <option key={r.value} value={r.value}>{r.label}</option>)}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Region</label>
                <select name="region" value={formData.region} onChange={handleChange} className="select-field">
                  <option value="">All Regions</option>
                  {REGIONS.map((r) => <option key={r.value} value={r.value}>{r.label}</option>)}
                </select>
              </div>
              <div>
                <label className="label">Crop (Optional)</label>
                <select name="crop" value={formData.crop} onChange={handleChange} className="select-field">
                  <option value="">All Crops</option>
                  {CROP_TYPES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
                </select>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Start Date</label>
                <input type="date" name="startDate" value={formData.startDate} onChange={handleChange} className="input-field" />
              </div>
              <div>
                <label className="label">End Date</label>
                <input type="date" name="endDate" value={formData.endDate} onChange={handleChange} className="input-field" />
              </div>
            </div>
            <div>
              <label className="label">Export Format</label>
              <div className="flex gap-3">
                {['pdf', 'csv', 'xlsx'].map((f) => (
                  <label key={f} className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="format"
                      value={f}
                      checked={formData.format === f}
                      onChange={handleChange}
                      className="w-4 h-4 text-primary-600 focus:ring-primary-500"
                    />
                    <span className="text-sm text-gray-700 uppercase font-medium">{f}</span>
                  </label>
                ))}
              </div>
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full py-2.5">
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Generating Report...
                </span>
              ) : 'Generate Report'}
            </button>
          </form>

          {generated && (
            <div className="mt-4 p-4 bg-green-50 rounded-lg border border-green-200 animate-fade-in">
              <div className="flex items-center gap-2 mb-2">
                <svg className="w-5 h-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="font-medium text-green-800">Report Ready</span>
              </div>
              <p className="text-sm text-green-700 mb-3">Your report has been generated successfully.</p>
              <button onClick={() => handleDownload('crop_health_report')} className="btn-primary text-sm">
                <svg className="w-4 h-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download Report
              </button>
            </div>
          )}
        </div>

        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Report History</h2>
          <div className="space-y-3">
            {reportHistory.map((report) => (
              <div
                key={report.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-start gap-3 min-w-0">
                  <div className="p-1.5 bg-white rounded-lg shadow-sm">
                    <svg className="w-5 h-5 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-gray-800 truncate">{report.name}</p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <span className="text-xs text-gray-400">{report.type}</span>
                      <span className="text-xs text-gray-300">|</span>
                      <span className="text-xs text-gray-400">{report.date}</span>
                      <span className="text-xs text-gray-300">|</span>
                      <span className="text-xs text-gray-400">{report.size}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2 flex-shrink-0">
                  {getStatusIcon(report.status)}
                  {report.status === 'Ready' && (
                    <button
                      onClick={() => handleDownload(report.name)}
                      className="p-1.5 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded transition-colors"
                      title="Download"
                    >
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                      </svg>
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
