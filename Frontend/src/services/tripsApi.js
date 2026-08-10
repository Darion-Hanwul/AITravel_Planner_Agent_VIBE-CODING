// src/services/tripsApi.js
import apiClient from './apiClient';

export const tripsApi = {
  async getTrips() {
    const response = await apiClient.get('/trips');
    return response.data;
  },

  async getTripById(id) {
    const response = await apiClient.get(`/trips/${id}`);
    return response.data;
  },

  async createTrip(tripData) {
    const response = await apiClient.post('/trips', tripData);
    return response.data;
  },

  async updateTrip(id, tripData) {
    const response = await apiClient.put(`/trips/${id}`, tripData);
    return response.data;
  },

  async deleteTrip(id) {
    const response = await apiClient.delete(`/trips/${id}`);
    return response.data;
  },
};

export default tripsApi;