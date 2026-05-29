import api from '../utils/api';

export const getAnalytics = async (params) => {
  const response = await api.get('/analytics', { params });
  return response.data;
};

export const getDashboardSummary = async () => {
  const response = await api.get('/analytics/dashboard-summary');
  return response.data;
};

export const getModelPerformance = async () => {
  const response = await api.get('/analytics/model-performance');
  return response.data;
};

export const explainPrediction = async (data) => {
  const response = await api.post('/analytics/explain-prediction', data);
  return response.data;
};
