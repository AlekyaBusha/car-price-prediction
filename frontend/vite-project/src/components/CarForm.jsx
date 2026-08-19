import { useEffect, useState } from "react";

import {
  fetchBrands,
  fetchModels,
  fetchFuelTypes,
  fetchTransmissions,
  fetchSellerTypes,
  fetchEngines,
  fetchSeats,
  fetchMaxPowers,
  predictPrice,
  predictOptions,
  explainPrice,
  forecastPrice,
} from "../services/api";

import SearchableDropdown from "./SearchableDropdown";

const DEFAULT_FUEL_TYPES = ["Petrol", "Diesel", "CNG", "Electric", "LPG"];
const DEFAULT_TRANSMISSIONS = ["Manual", "Automatic"];
const DEFAULT_SELLER_TYPES = ["Individual", "Dealer", "Trustmark Dealer"];
const DEFAULT_SEATS = [2, 4, 5, 6, 7, 8, 9];

function CarForm({
  onPrediction,
  onError,
  onFormDataChange,
  onExplanationLoading,
  onForecastLoading,
}) {
  // Dropdown option arrays
  const [brands, setBrands] = useState([]);
  const [models, setModels] = useState([]);
  const [fuelTypes, setFuelTypes] = useState(DEFAULT_FUEL_TYPES);
  const [transmissions, setTransmissions] = useState(DEFAULT_TRANSMISSIONS);
  const [sellerTypes, setSellerTypes] = useState(DEFAULT_SELLER_TYPES);
  const [engines, setEngines] = useState([]);
  const [maxPowers, setMaxPowers] = useState([]);
  const [seats, setSeats] = useState(DEFAULT_SEATS);

  // Form input state
  const [formData, setFormData] = useState({
    brand: "",
    model: "",
    fuel_type: "",
    transmission_type: "",
    seller_type: "",
    engine: "",
    max_power: "",
    seats: "",
    vehicle_age: 0,
    km_driven: 0,
    mileage: 5,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // AI suggestions state
  const [suggestions, setSuggestions] = useState({
    seats: [],
    engines: [],
    sellers: [],
  });

  // State for tracking model loading and no-model brands
  const [modelsLoading, setModelsLoading] = useState(false);
  const [modelsLoaded, setModelsLoaded] = useState(false);

  // Notify parent of form changes
  useEffect(() => {
    if (onFormDataChange) {
      onFormDataChange(formData);
    }
  }, [formData, onFormDataChange]);

  // Load brands on mount
  useEffect(() => {
    async function loadBrands() {
      try {
        const data = await fetchBrands();
        setBrands(Array.isArray(data) ? data : data?.brands || []);
      } catch (err) {
        console.error("Brand loading error:", err);
        setError("Failed to load brands.");
      }
    }
    loadBrands();
  }, []);

  // Load models & initial dependent options when brand changes
  useEffect(() => {
    async function loadModels() {
      if (!formData.brand) {
        setModels([]);
        setModelsLoaded(false);
        setFuelTypes(DEFAULT_FUEL_TYPES);
        setTransmissions(DEFAULT_TRANSMISSIONS);
        setSellerTypes(DEFAULT_SELLER_TYPES);
        setEngines([]);
        setMaxPowers([]);
        setSeats(DEFAULT_SEATS);
        return;
      }

      try {
        setModelsLoading(true);
        const data = await fetchModels(formData.brand);
        const modelList = Array.isArray(data) ? data : data?.models || [];
        setModels(modelList);
        setModelsLoaded(true);

        // Fetch brand-level dependent dropdown options
        const [
          fuelData,
          transmissionData,
          sellerData,
          engineData,
          maxPowerData,
          seatsData,
        ] = await Promise.all([
          fetchFuelTypes(formData.brand, ""),
          fetchTransmissions(formData.brand, ""),
          fetchSellerTypes(formData.brand, ""),
          fetchEngines(formData.brand, ""),
          fetchMaxPowers(formData.brand, ""),
          fetchSeats(formData.brand, ""),
        ]);

        setFuelTypes(fuelData?.fuel_types?.length ? fuelData.fuel_types : DEFAULT_FUEL_TYPES);
        setTransmissions(transmissionData?.transmission_types?.length ? transmissionData.transmission_types : DEFAULT_TRANSMISSIONS);
        setSellerTypes(sellerData?.seller_types?.length ? sellerData.seller_types : DEFAULT_SELLER_TYPES);
        setEngines(engineData?.engines || []);
        setMaxPowers(maxPowerData?.max_powers || []);
        setSeats(seatsData?.seats?.length ? seatsData.seats : DEFAULT_SEATS);

        if (modelList.length === 0) {
          setFormData((prev) => ({ ...prev, model: "No models" }));
        }
      } catch (err) {
        console.error("Model loading error:", err);
        setModels([]);
        setModelsLoaded(true);
        setFuelTypes(DEFAULT_FUEL_TYPES);
        setTransmissions(DEFAULT_TRANSMISSIONS);
        setSellerTypes(DEFAULT_SELLER_TYPES);
        setSeats(DEFAULT_SEATS);
      } finally {
        setModelsLoading(false);
      }
    }

    loadModels();
  }, [formData.brand]);

  // Load dependent dropdowns when Model is selected or typed
  useEffect(() => {
    async function loadModelOptions() {
      if (!formData.brand || !formData.model || formData.model === "No models") {
        return;
      }

      try {
        const [
          fuelData,
          transmissionData,
          sellerData,
          engineData,
          maxPowerData,
          seatsData,
        ] = await Promise.all([
          fetchFuelTypes(formData.brand, formData.model),
          fetchTransmissions(formData.brand, formData.model),
          fetchSellerTypes(formData.brand, formData.model),
          fetchEngines(formData.brand, formData.model),
          fetchMaxPowers(formData.brand, formData.model),
          fetchSeats(formData.brand, formData.model),
        ]);

        if (fuelData?.fuel_types?.length) setFuelTypes(fuelData.fuel_types);
        if (transmissionData?.transmission_types?.length) setTransmissions(transmissionData.transmission_types);
        if (sellerData?.seller_types?.length) setSellerTypes(sellerData.seller_types);
        if (engineData?.engines?.length) setEngines(engineData.engines);
        if (maxPowerData?.max_powers?.length) setMaxPowers(maxPowerData.max_powers);
        if (seatsData?.seats?.length) setSeats(seatsData.seats);
      } catch (err) {
        console.error("Dependent dropdown loading error:", err);
      }
    }

    loadModelOptions();
  }, [formData.brand, formData.model]);

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  async function handlePredict(event) {
    event.preventDefault();
    setError("");

    // Genuine required field validation
    if (!formData.brand || !formData.brand.trim()) {
      const errorMsg = "Please select a Brand.";
      setError(errorMsg);
      if (onError) onError(errorMsg);
      return;
    }

    if (models.length > 0 && (!formData.model || !formData.model.trim()) && formData.model !== "No models") {
      const errorMsg = "Please select or enter a Model.";
      setError(errorMsg);
      if (onError) onError(errorMsg);
      return;
    }

    if (!formData.fuel_type || !formData.fuel_type.trim()) {
      const errorMsg = "Please select a Fuel Type.";
      setError(errorMsg);
      if (onError) onError(errorMsg);
      return;
    }

    if (!formData.transmission_type || !formData.transmission_type.trim()) {
      const errorMsg = "Please select a Transmission.";
      setError(errorMsg);
      if (onError) onError(errorMsg);
      return;
    }

    if (!formData.seller_type || !formData.seller_type.trim()) {
      const errorMsg = "Please select a Seller Type.";
      setError(errorMsg);
      if (onError) onError(errorMsg);
      return;
    }

    try {
      setLoading(true);

      const payload = {
        brand: formData.brand,
        model: formData.model || "",
        fuel_type: formData.fuel_type || "Petrol",
        transmission_type: formData.transmission_type || "Manual",
        seller_type: formData.seller_type || "Individual",
        engine: formData.engine !== "" ? Number(formData.engine) : null,
        max_power: formData.max_power !== "" ? Number(formData.max_power) : null,
        seats: formData.seats !== "" ? Number(formData.seats) : null,
        vehicle_age: formData.vehicle_age !== "" ? Number(formData.vehicle_age) : 0,
        km_driven: formData.km_driven !== "" ? Number(formData.km_driven) : 0,
        mileage: formData.mileage !== "" ? Number(formData.mileage) : 5,
      };

      const result = await predictPrice(payload);

      let explanation = null;
      try {
        if (onExplanationLoading) onExplanationLoading(true);
        explanation = await explainPrice(payload);
      } catch (err) {
        console.error("SHAP explanation error:", err);
      } finally {
        if (onExplanationLoading) onExplanationLoading(false);
      }

      let forecast = [];
      try {
        if (onForecastLoading) onForecastLoading(true);
        const forecastResult = await forecastPrice(payload);
        forecast = forecastResult?.forecast || [];
      } catch (err) {
        console.error("Forecast error:", err);
      } finally {
        if (onForecastLoading) onForecastLoading(false);
      }

      const finalResult = {
        ...result,
        input: payload,
        explanation: explanation,
        forecast: forecast,
      };

      if (onPrediction) {
        onPrediction(finalResult);
      }

      // Check for suggestions if optional fields empty
      if (
        (formData.engine === "" || formData.engine === null) &&
        (formData.max_power === "" || formData.max_power === null) &&
        (formData.seats === "" || formData.seats === null)
      ) {
        fetchSuggestions(payload);
      }
    } catch (err) {
      console.error("Prediction error:", err);
      const errorMsg = err.message || "Failed to predict car price.";
      setError(errorMsg);
      if (onError) onError(errorMsg);
    } finally {
      setLoading(false);
    }
  }

  async function fetchSuggestions(payload) {
    try {
      const optResult = await predictOptions(payload);
      const options = optResult?.options || [];

      const seatsMap = {};
      options.forEach((o) => {
        const s = o.seats;
        if (!seatsMap[s] || o.predicted_price > seatsMap[s].predicted_price) {
          seatsMap[s] = o;
        }
      });
      const suggestedSeats = Object.values(seatsMap).sort((a, b) => a.seats - b.seats);

      const engineMap = {};
      options.forEach((o) => {
        const e = o.engine;
        if (!engineMap[e] || o.predicted_price > engineMap[e].predicted_price) {
          engineMap[e] = o;
        }
      });
      const suggestedEngines = Object.values(engineMap).sort((a, b) => Number(a.engine) - Number(b.engine));

      const sellers = [];
      for (const seller of sellerTypes.slice(0, 3)) {
        try {
          const sellerPayload = { ...payload, seller_type: seller };
          const r = await predictPrice(sellerPayload);
          sellers.push({ seller_type: seller, predicted_price: r.predicted_price });
        } catch {
          // ignore
        }
      }

      setSuggestions({ seats: suggestedSeats, engines: suggestedEngines, sellers });
    } catch (err) {
      console.error("Suggestion error", err);
    }
  }

  function handleReset() {
    setFormData({
      brand: "",
      model: "",
      fuel_type: "",
      transmission_type: "",
      seller_type: "",
      engine: "",
      max_power: "",
      seats: "",
      vehicle_age: 0,
      km_driven: 0,
      mileage: 5,
    });

    setModels([]);
    setFuelTypes([]);
    setTransmissions([]);
    setSellerTypes([]);
    setEngines([]);
    setMaxPowers([]);
    setSeats([]);
    setError("");
    setSuggestions({ seats: [], engines: [], sellers: [] });
  }

  return (
    <div
      style={{
        background: "var(--card-bg)",
        padding: "28px 24px",
        borderRadius: "12px",
        border: "1px solid var(--border)",
        color: "var(--text)",
      }}
    >
      <h2 style={{ margin: "0 0 4px 0", fontSize: "20px", fontWeight: 700, color: "#F8FAFC" }}>
        🚗 Vehicle Details
      </h2>

      <p style={{ color: "var(--muted-text)", margin: "0 0 20px 0", fontSize: "13px" }}>
        Enter the vehicle specifications to estimate market value and compare variants.
      </p>

      <form onSubmit={handlePredict}>
        {/* BRAND */}
        <SearchableDropdown
          label="Brand"
          options={brands}
          value={formData.brand}
          placeholder="🔍 Search brand..."
          required={true}
          onChange={(value) => {
            setFormData((previous) => ({
              ...previous,
              brand: value,
              model: "",
              fuel_type: "",
              transmission_type: "",
              seller_type: "",
              engine: "",
              max_power: "",
              seats: "",
            }));
            setModels([]);
            setFuelTypes([]);
            setTransmissions([]);
            setSellerTypes([]);
            setEngines([]);
            setMaxPowers([]);
            setSeats([]);
          }}
        />

        {/* MODEL */}
        <SearchableDropdown
          label="Model"
          options={models}
          value={formData.model}
          placeholder={
            !formData.brand
              ? "Select brand first"
              : modelsLoading
              ? "Loading models..."
              : modelsLoaded && models.length === 0
              ? "No models (type custom model)"
              : "🔍 Search or enter model..."
          }
          disabled={!formData.brand || modelsLoading}
          required={models.length > 0}
          onChange={(value) => {
            setFormData((previous) => ({
              ...previous,
              model: value,
            }));
          }}
        />

        {/* FUEL TYPE */}
        <SearchableDropdown
          label="Fuel Type"
          options={fuelTypes.length > 0 ? fuelTypes : DEFAULT_FUEL_TYPES}
          value={formData.fuel_type}
          placeholder={
            !formData.brand
              ? "Select brand first"
              : "🔍 Search fuel type..."
          }
          disabled={!formData.brand}
          required={true}
          onChange={(value) => {
            setFormData((previous) => ({
              ...previous,
              fuel_type: value,
            }));
          }}
        />

        {/* TRANSMISSION */}
        <SearchableDropdown
          label="Transmission"
          options={transmissions.length > 0 ? transmissions : DEFAULT_TRANSMISSIONS}
          value={formData.transmission_type}
          placeholder={
            !formData.brand
              ? "Select brand first"
              : "🔍 Search transmission..."
          }
          disabled={!formData.brand}
          required={true}
          onChange={(value) => {
            setFormData((previous) => ({
              ...previous,
              transmission_type: value,
            }));
          }}
        />

        {/* SELLER TYPE */}
        <SearchableDropdown
          label="Seller Type"
          options={sellerTypes.length > 0 ? sellerTypes : DEFAULT_SELLER_TYPES}
          value={formData.seller_type}
          placeholder={
            !formData.brand
              ? "Select brand first"
              : "🔍 Search seller type..."
          }
          disabled={!formData.brand}
          required={true}
          onChange={(value) => {
            setFormData((previous) => ({
              ...previous,
              seller_type: value,
            }));
          }}
        />

        {/* ENGINE (CC) */}
        <SearchableDropdown
          label="Engine (CC) (Optional)"
          options={engines}
          value={formData.engine}
          placeholder={
            !formData.brand
              ? "Select brand first"
              : "🔍 Search or type engine CC..."
          }
          disabled={!formData.brand}
          required={false}
          onChange={(value) => {
            setFormData((previous) => ({
              ...previous,
              engine: value,
            }));
          }}
        />

        {/* MAX POWER */}
        <SearchableDropdown
          label="Max Power (bhp) (Optional)"
          options={maxPowers}
          value={formData.max_power}
          placeholder={
            !formData.brand
              ? "Select brand first"
              : "🔍 Search or type max power..."
          }
          disabled={!formData.brand}
          required={false}
          onChange={(value) => {
            setFormData((previous) => ({
              ...previous,
              max_power: value,
            }));
          }}
        />

        {/* SEATS */}
        <SearchableDropdown
          label="Seats (Optional)"
          options={seats.length > 0 ? seats : DEFAULT_SEATS}
          value={formData.seats}
          placeholder={
            !formData.brand
              ? "Select brand first"
              : "🔍 Search or type seats..."
          }
          disabled={!formData.brand}
          required={false}
          onChange={(value) => {
            setFormData((previous) => ({
              ...previous,
              seats: value,
            }));
          }}
        />

        {/* VEHICLE AGE */}
        <div style={{ marginTop: "20px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px", fontSize: "13px", fontWeight: 600 }}>
            <span>Vehicle Age</span>
            <span style={{ color: "#38BDF8" }}>{Number(formData.vehicle_age || 0)} years</span>
          </div>
          <input
            type="range"
            name="vehicle_age"
            min="0"
            max="20"
            step="1"
            value={formData.vehicle_age || 0}
            onChange={handleChange}
            style={{ width: "100%", accentColor: "#2563EB", cursor: "pointer" }}
          />
        </div>

        {/* KM DRIVEN */}
        <div style={{ marginTop: "16px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px", fontSize: "13px", fontWeight: 600 }}>
            <span>KM Driven</span>
            <span style={{ color: "#38BDF8" }}>{Number(formData.km_driven || 0).toLocaleString()} km</span>
          </div>
          <input
            type="range"
            name="km_driven"
            min="0"
            max="300000"
            step="1000"
            value={formData.km_driven || 0}
            onChange={handleChange}
            style={{ width: "100%", accentColor: "#2563EB", cursor: "pointer" }}
          />
        </div>

        {/* MILEAGE */}
        <div style={{ marginTop: "16px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px", fontSize: "13px", fontWeight: 600 }}>
            <span>Mileage</span>
            <span style={{ color: "#38BDF8" }}>{Number(formData.mileage || 5).toFixed(1)} km/l</span>
          </div>
          <input
            type="range"
            name="mileage"
            min="5"
            max="40"
            step="0.1"
            value={formData.mileage || 5}
            onChange={handleChange}
            style={{ width: "100%", accentColor: "#2563EB", cursor: "pointer" }}
          />
        </div>

        {/* ERROR */}
        {error && (
          <div style={{ marginTop: "16px", padding: "10px 14px", borderRadius: "8px", background: "var(--danger-bg)", color: "var(--danger-text)", fontSize: "13px" }}>
            {error}
          </div>
        )}

        {/* ACTION BUTTONS */}
        <div style={{ display: "flex", gap: "12px", marginTop: "24px" }}>
          <button
            type="submit"
            disabled={loading}
            style={{
              flex: 1,
              padding: "12px 16px",
              border: "none",
              borderRadius: "8px",
              background: loading ? "#1E293B" : "#2563EB",
              color: loading ? "#94A3B8" : "white",
              fontSize: "14px",
              fontWeight: 700,
              cursor: loading ? "not-allowed" : "pointer",
              boxShadow: "0 4px 12px rgba(37, 99, 235, 0.3)",
              transition: "all 0.2s ease",
            }}
          >
            {loading ? "Estimating..." : "🚗 Predict Price"}
          </button>

          <button
            type="button"
            onClick={handleReset}
            style={{
              padding: "12px 18px",
              border: "1px solid var(--border)",
              borderRadius: "8px",
              background: "transparent",
              fontSize: "14px",
              color: "var(--text)",
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            Reset
          </button>
        </div>
      </form>
    </div>
  );
}

export default CarForm;