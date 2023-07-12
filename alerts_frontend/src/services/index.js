import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/alert';

export const fetchAlerts = async (page=1) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/?page=${page}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching alerts:', error);
    throw error;
  }
};

export const createAlert = async (newAlert) => {
  try {
    await axios.post(`${API_BASE_URL}/`, { ...newAlert });
  } catch (error) {
    console.error('Error creating alert:', error);
    throw error;
  }
};

export const updateAlert = async (alert) => {
  try {
    await axios.put(`${API_BASE_URL}/${alert.id}/`, alert);
  } catch (error) {
    console.error('Error updating alert:', error);
    throw error;
  }
};

export const deleteAlert = async (alertId) => {
  try {
    await axios.delete(`${API_BASE_URL}/${alertId}/`);
  } catch (error) {
    console.error('Error deleting alert:', error);
    throw error;
  }
};
