import { useState } from "react";
import Header from "../components/Header/Header";
import CarForm from "../components/CarForm.jsx";
import PriceRange from "../components/PriceRange.jsx";
import PriceCard from "../components/PriceCard.jsx";
import ShapExplanation from "../components/ShapExplanation.jsx";
import ForecastChartEnhanced from "../components/ForecastChartEnhanced.jsx";
import VariantComparison from "../components/VariantComparison.jsx";
import TimingRecommendation from "../components/TimingRecommendation.jsx";
import ErrorMessage from "../components/ErrorMessage.jsx";
import AboutSection from "../components/AboutSection.jsx";
import "../styles/Dashboard.css";

function Dashboard() {
  // Main state
  const [prediction, setPrediction] = useState(null);
  const [variants, setVariants] = useState([]);
  const [explanation, setExplanation] = useState(null);
  const [forecast, setForecast] = useState([]);

  // Loading states
  const [loading, setLoading] = useState(false);
  const [variantsLoading, setVariantsLoading] = useState(false);
  const [explanationLoading, setExplanationLoading] = useState(false);
  const [forecastLoading, setForecastLoading] = useState(false);

  // UI state
  const [activeTab, setActiveTab] = useState("variants"); // 'variants', 'shap', 'forecast'
  const [error, setError] = useState(null);

  const handlePrediction = (result) => {
    console.log("Dashboard received prediction:", result);

    // Set prediction price
    setPrediction(result);
    setError(null);

    // Set variants if available
    if (result.variants && result.variants.length > 0) {
      setVariants(result.variants);
    }

    // Set explanation if available
    if (result.explanation) {
      setExplanation(result.explanation);
    }

    // Set forecast if available
    if (result.forecast && result.forecast.length > 0) {
      setForecast(result.forecast);
    }
  };

  const handleError = (errorMessage) => {
    console.error("Dashboard error:", errorMessage);
    setError(errorMessage);
  };

  const handleClearError = () => {
    setError(null);
  };

  const handleVariantsLoading = (isLoading) => {
    setVariantsLoading(isLoading);
  };

  const handleExplanationLoading = (isLoading) => {
    setExplanationLoading(isLoading);
  };

  const handleForecastLoading = (isLoading) => {
    setForecastLoading(isLoading);
  };

  const hasResults = prediction !== null;
  const hasVariants = variants && variants.length > 0;
  const hasExplanation = explanation && explanation.top_features;
  const hasForecast = forecast && forecast.length > 0;

  return (
    <>
      <Header />

      {error && (
        <div className="error-section">
          <ErrorMessage message={error} onDismiss={handleClearError} />
        </div>
      )}

      <main className="dashboard-container">
        <div className="dashboard-layout">
          {/* Left Column: Form */}
          <aside className="form-column">
            <CarForm
              onPrediction={handlePrediction}
              onError={handleError}
              onVariantsLoading={handleVariantsLoading}
              onExplanationLoading={handleExplanationLoading}
              onForecastLoading={handleForecastLoading}
            />
          </aside>

          {/* Right Column: Results */}
          <section className="results-column">
            {!hasResults ? (
              <div className="empty-state">
                <div className="empty-icon">🚗</div>
                <h2>Enter car details to get started</h2>
                <p>
                  Fill in the form on the left to predict prices, view variants,
                  and get AI-powered insights.
                </p>
              </div>
            ) : (
              <>
                {/* Price Range Card */}
                <div className="prediction-card">
                  <PriceRange data={prediction.price_range || {
                    low: prediction.predicted_price,
                    predicted: prediction.predicted_price,
                    high: prediction.predicted_price,
                  }} />
                </div>

                {/* Tab Navigation */}
                {(hasVariants || hasExplanation || hasForecast) && (
                  <div className="tabs-container">
                    <div className="tabs">
                      {hasVariants && (
                        <button
                          className={`tab ${activeTab === "variants" ? "active" : ""}`}
                          onClick={() => setActiveTab("variants")}
                        >
                          Variants
                          {hasVariants && <span className="badge">{variants.length}</span>}
                        </button>
                      )}

                      {hasExplanation && (
                        <button
                          className={`tab ${activeTab === "shap" ? "active" : ""}`}
                          onClick={() => setActiveTab("shap")}
                        >
                          Explanation
                        </button>
                      )}

                      {hasForecast && (
                        <button
                          className={`tab ${activeTab === "forecast" ? "active" : ""}`}
                          onClick={() => setActiveTab("forecast")}
                        >
                          Forecast
                        </button>
                      )}
                    </div>
                  </div>
                )}

                {/* Tab Content */}
                {hasVariants && activeTab === "variants" && (
                  <div className="tab-content">
                    <VariantComparison
                      variants={variants}
                      loading={variantsLoading}
                    />
                  </div>
                )}

                {hasExplanation && activeTab === "shap" && (
                  <div className="tab-content">
                    <ShapExplanation
                      explanation={explanation}
                      loading={explanationLoading}
                    />
                  </div>
                )}

                {hasForecast && activeTab === "forecast" && (
                  <div className="tab-content">
                    <ForecastChartEnhanced
                      forecast={forecast}
                      loading={forecastLoading}
                    />
                    {forecast && forecast.length > 0 && (
                      <TimingRecommendation forecast={forecast} />
                    )}
                  </div>
                )}
              </>
            )}
          </section>
        </div>

        {/* About Section */}
        <AboutSection />
      </main>
    </>
  );
}

export default Dashboard;