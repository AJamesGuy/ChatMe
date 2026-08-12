import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:5000";

const axiosInstance = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests automatically if it exists in localStorage
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  }
);

// Handle errors globally
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle specific status codes if needed
      switch (error.response?.status) {
        case 401:
          // Handle unauthorized access, e.g., redirect to login
          localStorage.removeItem("token");
          window.location.href = "/login";
          break;
        case 403:
          // Handle forbidden access
          localStorage.removeItem("token");
          window.location.href = "/login";
          break;
        case 500:
          // Handle server errors
          localStorage.removeItem("token");
          window.location.href = "/login";
          break;
        default:
            localStorage.removeItem("token");
            window.location.href = "/login";
            break;
      }
    }
    return Promise.reject(error);
  }
);

//API Endpoint Logic


