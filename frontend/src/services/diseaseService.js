import api from '../utils/api';

export const diseaseRisk = async (data) => {
  const response = await api.post('/disease/risk', data);
  return response.data;
};

export const batchDiseaseRisk = async (crops) => {
  const response = await api.post('/disease/batch', crops);
  return response.data;
};
