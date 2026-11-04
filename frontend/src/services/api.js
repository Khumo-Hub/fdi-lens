import axios from "axios";
import * as demoApi from "./demoApi";


// Enable this only for the standalone HTML/CSS/JavaScript portfolio preview.
// The existing live FastAPI integration remains the default.
export const IS_DEMO_MODE = import.meta.env.VITE_DEMO_MODE === "true";
const API_BASE_URL = import.meta.env.VITE_API_URL;

if (!IS_DEMO_MODE && !API_BASE_URL) {
  throw new Error(
    "VITE_API_URL is not configured. " +
    "Set VITE_API_URL or enable VITE_DEMO_MODE=true for a standalone preview."
  );
}

const api = IS_DEMO_MODE ? null : axios.create({ baseURL: API_BASE_URL });

const liveGet = async (path, params) => {
  const response = await api.get(path, params ? { params } : undefined);
  return response.data;
};

export const getSummary = () =>
  IS_DEMO_MODE ? demoApi.getSummary() : liveGet("/api/analytics/summary");

export const getTopDestinations = () =>
  IS_DEMO_MODE
    ? demoApi.getTopDestinations()
    : liveGet("/api/analytics/top-destinations", { limit: 10 });

export const getTopSectors = () =>
  IS_DEMO_MODE
    ? demoApi.getTopSectors()
    : liveGet("/api/analytics/top-sectors", { limit: 10 });

export const getTrends = () =>
  IS_DEMO_MODE ? demoApi.getTrends() : liveGet("/api/analytics/trends");

export const getProjects = (params = {}) =>
  IS_DEMO_MODE ? demoApi.getProjects(params) : liveGet("/api/projects", params);

export const getMapData = () =>
  IS_DEMO_MODE ? demoApi.getMapData() : liveGet("/api/analytics/map");

export const searchGlobal = (query, limit = 5) =>
  IS_DEMO_MODE
    ? demoApi.searchGlobal(query, limit)
    : liveGet("/api/search", { q: query, limit });

export default api;
