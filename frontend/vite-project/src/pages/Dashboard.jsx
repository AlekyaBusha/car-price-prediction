import { useState, useCallback } from "react";
import Header from "../components/Header/Header";
import CarForm from "../components/CarForm.jsx";
import PriceRange from "../components/PriceRange.jsx";
import ShapExplanation from "../components/ShapExplanation.jsx";
import ForecastChartEnhanced from "../components/ForecastChartEnhanced.jsx";
import VariantComparison from "../components/VariantComparison.jsx";
import TimingRecommendation from "../components/TimingRecommendation.jsx";
import ErrorMessage from "../components/ErrorMessage.jsx";
import AboutSection from "../components/AboutSection.jsx";
import { predictVariants } from "../services/api";
import "../styles/Dashboard.css";

function Dashboard() {
  // Top-level Navigation state
  const [activeNav, setActiveNav] = useState("predict");

  // Main prediction state
  const [prediction, setPrediction] = useState(null);
  const [variants, setVariants] = useState([]);
  const [explanation, setExplanation] = useState(null);
  const [forecast, setForecast] = useState([]);

  // Current form inputs
  const [currentFormData, setCurrentFormData] = useState({
    brand: "",
    model: "",
    vehicle_age: 0,
    km_driven: 0,
    mileage: 5,
    engine: "",
    seats: "",
  });

  // Loading states
  const [variantsLoading, setVariantsLoading] = useState(false);
  const [explanationLoading, setExplanationLoading] = useState(false);
  const [forecastLoading, setForecastLoading] = useState(false);

  // Tab state - default to 'variants' (Compare Variants)
  const [activeTab, setActiveTab] = useState("variants");
  const [error, setError] = useState(null);

  const handleFormDataChange = useCallback((formData) => {
    setCurrentFormData(formData);
  }, []);

  const handleSelectNav = (navId) => {
    setActiveNav("predict");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Fetch variants for selected Brand + Model
  const handleFetchVariants = async (formDataOverride = null) => {
    const data = formDataOverride || currentFormData;
    if (!data.brand || !data.model) {
      setError("Please select Brand and Model to compare variants.");
      return;
    }

    try {
      setVariantsLoading(true);
      setError(null);

      const payload = {
        brand: data.brand,
        model: data.model,
        vehicle_age: data.vehicle_age !== "" ? Number(data.vehicle_age) : 0,
        km_driven: data.km_driven !== "" ? Number(data.km_driven) : 0,
        mileage: data.mileage !== "" ? Number(data.mileage) : 5,
        engine: data.engine !== "" && data.engine !== null ? Number(data.engine) : null,
        seats: data.seats !== "" && data.seats !== null ? Number(data.seats) : null,
      };

      const result = await predictVariants(payload);
      const variantList = result?.variants || [];
      setVariants(variantList);

      if (variantList.length === 0) {
        setError(`No variants found for ${data.brand} ${data.model}.`);
      }
    } catch (err) {
      console.error("Variant fetch error:", err);
      setError(err.message || "Failed to load variants.");
    } finally {
      setVariantsLoading(false);
    }
  };

  const handlePrediction = (result) => {
    setPrediction(result);
    setError(null);

    // Keep Compare Variants as the active tab
    setActiveTab("variants");

    if (result.explanation) {
      setExplanation(result.explanation);
    }

    if (result.forecast && result.forecast.length > 0) {
      setForecast(result.forecast);
    }

    // Automatically load variants for the predicted car
    if (result.input?.brand && result.input?.model) {
      handleFetchVariants(result.input);
    }
  };

  const handleError = (errorMessage) => {
    console.error("Dashboard error:", errorMessage);
    setError(errorMessage);
  };

  const handleClearError = () => {
    setError(null);
  };

  const hasResults = prediction !== null;
  const hasVariants = variants && variants.length > 0;
  const hasExplanation = explanation && (explanation.top_features || Array.isArray(explanation));
  const hasForecast = forecast && forecast.length > 0;

  return (
    <>
      <Header
        activeNav={activeNav}
        onSelectNav={handleSelectNav}
      />

      {error && (
        <div className="error-section">
          <ErrorMessage message={error} onDismiss={handleClearError} />
        </div>
      )}

      <main className="dashboard-container">
        <div className="dashboard-layout">
          {/* Left Column: Vehicle Details Form */}
          <aside className="form-column">
            <CarForm
              onPrediction={handlePrediction}
              onError={handleError}
              onFormDataChange={handleFormDataChange}
              onExplanationLoading={setExplanationLoading}
              onForecastLoading={setForecastLoading}
            />
          </aside>

          {/* Right Column: Prediction & Tabs */}
          <section className="results-column">
            {!hasResults && !hasVariants ? (
              <div className="empty-state">
                <div className="empty-icon">🚗</div>
                <h2>Enter Vehicle Details to Predict & Compare</h2>
                <p>
                  Fill in the vehicle specifications on the left to estimate market price,
                  explore all available trims in the Variant Comparison, and view AI insights.
                </p>
                {currentFormData.brand && currentFormData.model && (
                  <button
                    type="button"
                    className="btn-compare-prompt"
                    style={{ marginTop: "12px" }}
                    onClick={() => {
                      handleFetchVariants();
                      setActiveTab("variants");
                    }}
                    disabled={variantsLoading}
                  >
                    {variantsLoading ? "Loading Variants..." : "🔍 Compare All Variants for Selected Model"}
                  </button>
                )}
              </div>
            ) : (
              <>
                {/* Predicted Price Range Card */}
                {hasResults && (
                  <div className="prediction-card">
                    <PriceRange
                      data={
                        prediction.price_range || {
                          low: prediction.predicted_price,
                          predicted: prediction.predicted_price,
                          high: prediction.predicted_price,
                        }
                      }
                    />
                  </div>
                )}

                {/* Right Side Navigation Tabs: 1. Compare Variants  2. SHAP Explanation  3. Future Forecast */}
                <div className="tabs-container">
                  <div className="tabs">
                    <button
                      type="button"
                      className={`tab ${activeTab === "variants" ? "active" : ""}`}
                      onClick={() => setActiveTab("variants")}
                    >
                      Compare Variants
                      {hasVariants && <span className="badge">{variants.length}</span>}
                    </button>

                    <button
                      type="button"
                      className={`tab ${activeTab === "shap" ? "active" : ""}`}
                      onClick={() => setActiveTab("shap")}
                    >
                      SHAP Explanation
                    </button>

                    <button
                      type="button"
                      className={`tab ${activeTab === "forecast" ? "active" : ""}`}
                      onClick={() => setActiveTab("forecast")}
                    >
                      Future Forecast
                    </button>
                  </div>
                </div>

                {/* Tab Content in Matching Order */}
                {activeTab === "variants" && (
                  <div className="tab-content">
                    <VariantComparison
                      variants={variants}
                      loading={variantsLoading}
                      onCompareAllVariants={() => handleFetchVariants()}
                      isComparing={variantsLoading}
                      hasModelSelected={!!(currentFormData.brand && currentFormData.model)}
                    />
                  </div>
                )}

                {activeTab === "shap" && (
                  <div className="tab-content">
                    <ShapExplanation
                      explanation={explanation}
                      loading={explanationLoading}
                    />
                  </div>
                )}

                {activeTab === "forecast" && (
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