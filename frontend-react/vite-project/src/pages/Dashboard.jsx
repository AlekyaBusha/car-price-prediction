import React, { useState } from "react";

import Header from "../components/Header/Header";
import CarForm from "../components/CarForm";
import PriceCard from "../components/PriceCard";
import ShapChart from "../components/ShapChart";
import ForecastChart from "../components/ForecastChart";

import {
  predictCar,
  forecastCar,
  explainCar,
} from "../services/api";


function Dashboard() {
  const [prediction, setPrediction] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [contributions, setContributions] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  async function handlePredict(carData) {
    setLoading(true);
    setError("");

    try {
      // Prediction
      const predictionResponse = await predictCar(carData);

      const predictionData =
        predictionResponse?.data ||
        predictionResponse;

      setPrediction(predictionData);


      // Forecast
      try {
        const forecastResponse = await forecastCar(carData);

        const forecastData =
          forecastResponse?.data ||
          forecastResponse;

        setForecast(
          forecastData?.forecast ||
          forecastData ||
          []
        );
      } catch (forecastError) {
        console.error(
          "Forecast error:",
          forecastError
        );
      }


      // SHAP Explanation
      try {
        const explainResponse = await explainCar(carData);

        const explainData =
          explainResponse?.data ||
          explainResponse;

        setContributions(
          explainData?.contributions ||
          explainData?.top_features ||
          []
        );
      } catch (explainError) {
        console.error(
          "Explainability error:",
          explainError
        );
      }

    } catch (err) {
      console.error(err);

      setError(
        err.message ||
        "Unable to generate prediction."
      );
    } finally {
      setLoading(false);
    }
  }


  return (
    <div className="dashboard">

      {/* Header */}
      <Header />


      {/* Main Content */}
      <main className="dashboard-container">

        {/* Error */}
        {error && (
          <div className="dashboard-error">
            <strong>Error:</strong> {error}
          </div>
        )}


        {/* Top Section */}
        <div className="top-grid">

          <CarForm
            onPredict={handlePredict}
            loading={loading}
          />

          <PriceCard
            prediction={prediction}
            loading={loading}
          />

        </div>


        {/* Bottom Section */}
        <div className="bottom-grid">

          <ShapChart
            contributions={contributions}
          />

          <ForecastChart
            forecast={forecast}
          />

        </div>


        {/* Footer */}
        <footer className="dashboard-footer">

          <div>
            <strong>
              AI Car Price Prediction
            </strong>

            <span>
              Machine Learning Powered Vehicle Valuation
            </span>
          </div>

          <div>
            © 2026 AI Car Price Prediction
          </div>

        </footer>

      </main>

    </div>
  );
}


export default Dashboard;