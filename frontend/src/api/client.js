import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

export const getPersonas = () => apiClient.get("/personas").then((res) => res.data);

export const getSessions = () => apiClient.get("/sessions").then((res) => res.data);

export const getSession = (sessionId) =>
  apiClient.get(`/sessions/${sessionId}`).then((res) => res.data);

export const startRun = (payload) =>
  apiClient.post("/runs", payload).then((res) => res.data);

export default apiClient;