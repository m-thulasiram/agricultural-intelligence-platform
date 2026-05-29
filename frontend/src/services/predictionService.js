import api from '../utils/api';

export const predictCropHealth = async (data) => {
  const response = await api.post('/predict', data);
  return response.data;
};

export const batchPredict = async (predictions) => {
  const response = await api.post('/predict/batch', predictions);
  return response.data;
};

export const getFeatureImportance = async () => {
  const response = await api.get('/analytics/feature-importance');
  return response.data;
};
