import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});


export const getSummary = async () => {
  const response = await api.get(
    "/api/analytics/summary"
  );

  return response.data;
};


export const getTopDestinations = async () => {
  const response = await api.get(
    "/api/analytics/top-destinations?limit=10"
  );

  return response.data;
};


export const getTopSectors = async () => {
  const response = await api.get(
    "/api/analytics/top-sectors?limit=10"
  );

  return response.data;
};


export const getTrends = async () => {
  const response = await api.get(
    "/api/analytics/trends"
  );

  return response.data;
};


export default api;