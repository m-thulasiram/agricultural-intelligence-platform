import api from '../utils/api';

export const cropRecommendation = async (data) => {
  const response = await api.post('/recommendation/crop', data);
  return response.data;
};

export const fertilizerPlan = async (data) => {
  const response = await api.post('/recommendation/fertilizer', data);
  return response.data;
};

export const irrigationSchedule = async (data) => {
  const response = await api.post('/recommendation/irrigation', data);
  return response.data;
};
