import axios from "axios";


const API_BASE_URL =
  import.meta.env.VITE_API_URL;


if (!API_BASE_URL) {
  throw new Error(
    "VITE_API_URL is not configured. " +
    "Add it to the frontend environment file."
  );
}


const api = axios.create({
  baseURL: API_BASE_URL,
});


export const getSummary = async () => {

  const response = await api.get(
    "/api/analytics/summary"
  );

  return response.data;
};


export const getTopDestinations =
  async () => {

    const response = await api.get(
      "/api/analytics/top-destinations",
      {
        params: {
          limit: 10,
        },
      }
    );

    return response.data;
  };


export const getTopSectors =
  async () => {

    const response = await api.get(
      "/api/analytics/top-sectors",
      {
        params: {
          limit: 10,
        },
      }
    );

    return response.data;
  };


export const getTrends = async () => {

  const response = await api.get(
    "/api/analytics/trends"
  );

  return response.data;
};


export const getProjects =
  async (params = {}) => {

    const response = await api.get(
      "/api/projects",
      {
        params,
      }
    );

    return response.data;
  };


export const getMapData =
  async () => {

    const response = await api.get(
      "/api/analytics/map"
    );

    return response.data;
  };


export default api;