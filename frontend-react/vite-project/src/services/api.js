import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});


// ===============================
// Get Brands
// ===============================

export async function getBrands() {
  return api.get("/brands");
}


// ===============================
// Get Models
// ===============================

export async function getModels(brand) {
  return api.get("/models", {
    params: {
      brand: brand,
    },
  });
}


// ===============================
// Predict Car Price
// ===============================

export async function predictCar(carData) {
  return api.post("/predict", carData);
}


// ===============================
// Future Price Forecast
// ===============================

export async function forecastCar(carData) {
  return api.post("/forecast", carData);
}


// ===============================
// SHAP Explanation
// ===============================

export async function explainCar(carData) {
  return api.post("/explain", carData);
}


export default api;