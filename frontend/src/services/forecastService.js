import api from '../utils/api';

export const futureForecast = async (data) => {
  const response = await api.post('/forecast/future', data);
  return response.data;
};

export const compareModels = async (data) => {
  const response = await api.post('/forecast/compare-models', data);
  return response.data;
};

export const getForecastHistory = async (region) => {
  const response = await api.get(`/forecast/history/${region}`);
  return response.data;
};

export const getDynamicTimeline = async (data) => {
  const response = await api.post('/forecast/timeline', data);
  return response.data;
};
