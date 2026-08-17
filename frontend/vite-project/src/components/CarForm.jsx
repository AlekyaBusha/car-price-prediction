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
  predictVariants,
  predictOptions,
  explainPrice,
  forecastPrice,
} from "../services/api";

import SearchableDropdown from "./SearchableDropdown";


function CarForm({
  onPrediction,
  onError,
  onVariantsLoading,
  onExplanationLoading,
  onForecastLoading,
}) {

  // =========================================================
  // Dropdown data
  // =========================================================

  const [brands, setBrands] = useState([]);
  const [models, setModels] = useState([]);

  const [fuelTypes, setFuelTypes] = useState([]);
  const [transmissions, setTransmissions] = useState([]);
  const [sellerTypes, setSellerTypes] = useState([]);

  const [engines, setEngines] = useState([]);
  const [maxPowers, setMaxPowers] = useState([]);
  const [seats, setSeats] = useState([]);


  // =========================================================
  // Form data
  // =========================================================

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


  // =========================================================
  // Prediction state
  // =========================================================

  const [prediction, setPrediction] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  // =========================================================
  // Variant state
  // =========================================================

  const [variants, setVariants] = useState([]);

  const [variantLoading, setVariantLoading] =
    useState(false);

  const [variantError, setVariantError] =
    useState("");

  // =========================================================
  // Suggestion state (AI Suggestions)
  // =========================================================

  const [suggestions, setSuggestions] = useState({
    seats: [],
    engines: [],
    sellers: [],
  });

  const [suggestionLoading, setSuggestionLoading] =
    useState(false);


  // =========================================================
  // Load brands
  // =========================================================

  useEffect(() => {

    async function loadBrands() {

      try {

        const data = await fetchBrands();

        setBrands(
          Array.isArray(data)
            ? data
            : data?.brands || []
        );

      } catch (err) {

        console.error(
          "Brand loading error:",
          err
        );

        setError(
          "Failed to load brands."
        );

      }

    }

    loadBrands();

  }, []);


  // =========================================================
  // Load models when brand changes
  // =========================================================

  useEffect(() => {

    async function loadModels() {

      if (!formData.brand) {

        setModels([]);

        return;

      }

      try {

        const data =
          await fetchModels(
            formData.brand
          );

        setModels(
          Array.isArray(data)
            ? data
            : data?.models || []
        );

      } catch (err) {

        console.error(
          "Model loading error:",
          err
        );

        setModels([]);

      }

    }

    loadModels();

  }, [formData.brand]);


  // =========================================================
  // Load options based on Brand + Model
  // =========================================================

  useEffect(() => {

    async function loadModelOptions() {

      if (
        !formData.brand ||
        !formData.model
      ) {

        setFuelTypes([]);
        setTransmissions([]);
        setSellerTypes([]);
        setEngines([]);
        setMaxPowers([]);
        setSeats([]);

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

          fetchFuelTypes(
            formData.brand,
            formData.model
          ),

          fetchTransmissions(
            formData.brand,
            formData.model
          ),

          fetchSellerTypes(
            formData.brand,
            formData.model
          ),

          fetchEngines(
            formData.brand,
            formData.model
          ),

          fetchMaxPowers(
            formData.brand,
            formData.model
          ),

          fetchSeats(
            formData.brand,
            formData.model
          ),

        ]);


        setFuelTypes(
          fuelData?.fuel_types || []
        );

        setTransmissions(
          transmissionData?.transmission_types || []
        );

        setSellerTypes(
          sellerData?.seller_types || []
        );

        setEngines(
          engineData?.engines || []
        );

        setMaxPowers(
          maxPowerData?.max_powers || []
        );

        setSeats(
          seatsData?.seats || []
        );


        console.log(
          "Model-dependent options loaded:"
        );

        console.log({

          brand:
            formData.brand,

          model:
            formData.model,

          fuelTypes:
            fuelData?.fuel_types || [],

          transmissions:
            transmissionData?.transmission_types || [],

          sellerTypes:
            sellerData?.seller_types || [],

          engines:
            engineData?.engines || [],

          maxPowers:
            maxPowerData?.max_powers || [],

          seats:
            seatsData?.seats || [],

        });

      } catch (err) {

        console.error(
          "Dependent dropdown loading error:",
          err
        );

        setFuelTypes([]);
        setTransmissions([]);
        setSellerTypes([]);
        setEngines([]);
        setMaxPowers([]);
        setSeats([]);

      }

    }

    loadModelOptions();

  }, [
    formData.brand,
    formData.model
  ]);


  // =========================================================
  // Normal input handler
  // =========================================================

  function handleChange(event) {

    const {
      name,
      value
    } = event.target;


    setFormData((previous) => ({

      ...previous,

      [name]: value,

    }));

  }


  // =========================================================
  // Normal price prediction
  // =========================================================

  async function handlePredict(event) {

    event.preventDefault();

    setError("");

    setPrediction(null);


    // =======================================================
    // Required validation
    // =======================================================

    if (
      !formData.brand ||
      !formData.model ||
      !formData.fuel_type ||
      !formData.transmission_type ||
      !formData.seller_type
    ) {

      const errorMsg = "Please fill Brand, Model, Fuel Type, Transmission and Seller Type.";
      setError(errorMsg);
      if (onError) onError(errorMsg);
      return;

    }


    try {

      setLoading(true);


      // =====================================================
      // Prediction payload
      // =====================================================

      const payload = {

        brand:
          formData.brand,

        model:
          formData.model,

        fuel_type:
          formData.fuel_type,

        transmission_type:
          formData.transmission_type,

        seller_type:
          formData.seller_type,


        // Optional
        engine:
          formData.engine !== ""
            ? Number(formData.engine)
            : null,


        // Optional
        max_power:
          formData.max_power !== ""
            ? Number(formData.max_power)
            : null,


        // Optional
        seats:
          formData.seats !== ""
            ? Number(formData.seats)
            : null,


        // Default 0
        vehicle_age:
          formData.vehicle_age !== ""
            ? Number(formData.vehicle_age)
            : 0,


        // Default 0
        km_driven:
          formData.km_driven !== ""
            ? Number(formData.km_driven)
            : 0,


        // Default 5
        mileage:
          formData.mileage !== ""
            ? Number(formData.mileage)
            : 5,

      };


      console.log(
        "Prediction request:"
      );

      console.log(payload);


      // =====================================================
      // Prediction
      // =====================================================

      const result =
        await predictPrice(
          payload
        );


      console.log(
        "Prediction response:"
      );

      console.log(result);


      // =====================================================
      // SHAP
      // =====================================================

      let explanation = null;

      try {
        if (onExplanationLoading) onExplanationLoading(true);

        const explanationResult =
          await explainPrice(
            payload
          );

        console.log(
          "SHAP explanation response:"
        );

        console.log(
          explanationResult
        );

        explanation =
          explanationResult;

      } catch (err) {

        console.error(
          "SHAP explanation error:",
          err
        );
      } finally {
        if (onExplanationLoading) onExplanationLoading(false);
      }


      // =====================================================
      // Forecast
      // =====================================================

      let forecast = [];

      try {
        if (onForecastLoading) onForecastLoading(true);

        const forecastResult =
          await forecastPrice(
            payload
          );

        console.log(
          "Forecast response:"
        );

        console.log(
          forecastResult
        );

        forecast =
          forecastResult?.forecast || [];

      } catch (err) {

        console.error(
          "Forecast error:",
          err
        );
      } finally {
        if (onForecastLoading) onForecastLoading(false);
      }


      // =====================================================
      // Final result
      // =====================================================

      const finalResult = {

        ...result,

        input:
          payload,

        explanation:
          explanation,

        forecast:
          forecast,

      };


      setPrediction(
        finalResult
      );


      if (onPrediction) {

        onPrediction(
          finalResult
        );

      }

      // If engine, max_power and seats not provided, fetch AI suggestions
      if (
        (formData.engine === "" || formData.engine === null) &&
        (formData.max_power === "" || formData.max_power === null) &&
        (formData.seats === "" || formData.seats === null)
      ) {

        const suggestionPayload = {
          brand: formData.brand,
          model: formData.model,

          // CarInput required fields: use selected or fallback to first available option or 'unknown'
          fuel_type:
            formData.fuel_type || (fuelTypes && fuelTypes[0]) || "unknown",

          transmission_type:
            formData.transmission_type || (transmissions && transmissions[0]) || "unknown",

          seller_type:
            formData.seller_type || (sellerTypes && sellerTypes[0]) || "unknown",

          vehicle_age:
            formData.vehicle_age !== ""
              ? Number(formData.vehicle_age)
              : 0,
          km_driven:
            formData.km_driven !== ""
              ? Number(formData.km_driven)
              : 0,
          mileage:
            formData.mileage !== ""
              ? Number(formData.mileage)
              : 5,
        };

        fetchSuggestions(suggestionPayload);

      }

    } catch (err) {

      console.error(
        "Prediction error:",
        err
      );

      const errorMsg = err.message || "Failed to predict car price.";
      setError(errorMsg);
      if (onError) onError(errorMsg);

    } finally {

      setLoading(false);

    }

  }


  // =========================================================
  // Fetch AI Suggestions when engine,max_power,seats are not selected
  // =========================================================

  async function fetchSuggestions(payload) {

    try {

      setSuggestionLoading(true);

      // Call backend predict/options endpoint
      const optResult = await predictOptions(payload);

      const options = optResult?.options || [];

      // Seats suggestions: pick highest predicted price per seats
      const seatsMap = {};

      options.forEach((o) => {
        const s = o.seats;
        if (!seatsMap[s] || o.predicted_price > seatsMap[s].predicted_price) {
          seatsMap[s] = o;
        }
      });

      const seats = Object.values(seatsMap).sort((a,b)=>a.seats-b.seats);

      // Engine suggestions: highest predicted price per engine
      const engineMap = {};

      options.forEach((o) => {
        const e = o.engine;
        if (!engineMap[e] || o.predicted_price > engineMap[e].predicted_price) {
          engineMap[e] = o;
        }
      });

      const engines = Object.values(engineMap).sort((a,b)=>Number(a.engine)-Number(b.engine));

      // Seller suggestions: use existing sellerTypes and predictPrice for each
      const sellers = [];

      for (const seller of sellerTypes.slice(0,3)) {

        try {
          const sellerPayload = { ...payload, seller_type: seller };

          const r = await predictPrice(sellerPayload);

          sellers.push({ seller_type: seller, predicted_price: r.predicted_price });

        } catch (err) {
          // ignore per-seller failures
        }

      }

      setSuggestions({ seats, engines, sellers });

    } catch (err) {

      console.error('Suggestion error', err);

    } finally {

      setSuggestionLoading(false);

    }

  }


  // =========================================================
  // VARIANT PREDICTION
  // =========================================================

  async function handleVariantPrediction() {

    setVariantError("");

    setVariants([]);


    // -------------------------------------------------------
    // Only Brand + Model are required
    // -------------------------------------------------------

    if (
      !formData.brand ||
      !formData.model
    ) {

      setVariantError(
        "Please select Brand and Model first."
      );

      return;

    }


    try {

      setVariantLoading(true);
      if (onVariantsLoading) onVariantsLoading(true);


      // -----------------------------------------------------
      // Variant payload
      // -----------------------------------------------------

      const payload = {

        brand:
          formData.brand,

        model:
          formData.model,

        vehicle_age:
          formData.vehicle_age !== ""
            ? Number(formData.vehicle_age)
            : 0,

        km_driven:
          formData.km_driven !== ""
            ? Number(formData.km_driven)
            : 0,

        mileage:
          formData.mileage !== ""
            ? Number(formData.mileage)
            : 5,
        // Optional engine and seats for variant comparison
        engine:
          formData.engine !== ""
            ? Number(formData.engine)
            : null,

        seats:
          formData.seats !== ""
            ? Number(formData.seats)
            : null,

      };


      console.log(
        "================================="
      );

      console.log(
        "Variant prediction request:"
      );

      console.log(payload);


      // -----------------------------------------------------
      // API request
      // -----------------------------------------------------

      const result =
        await predictVariants(
          payload
        );


      console.log(
        "Variant prediction response:"
      );

      console.log(result);


      // -----------------------------------------------------
      // Store variants
      // -----------------------------------------------------

      const variantResults =
        result?.variants ||
        result?.options ||
        [];


      setVariants(
        variantResults
      );


      // -----------------------------------------------------
      // No results
      // -----------------------------------------------------

      if (
        variantResults.length === 0
      ) {

        setVariantError(
          "No variants were found for this Brand and Model."
        );

      }

    } catch (err) {

      console.error(
        "Variant prediction error:",
        err
      );


      setVariantError(
        err.message ||
        "Failed to predict variants."
      );

    } finally {

      setVariantLoading(false);
      if (onVariantsLoading) onVariantsLoading(false);

    }

  }


  // =========================================================
  // Reset
  // =========================================================

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


    setPrediction(null);

    setVariants([]);

    setVariantError("");

    setError("");

  }


  // =========================================================
  // UI
  // =========================================================

  return (

    <div
      style={{
        background: "var(--card-bg)",
        padding: "40px",
        borderRadius: "16px",
        boxShadow:
          "0 10px 25px rgba(0,0,0,0.08)",
        color: "var(--text)",
      }}
    >

      <h2>
        🚘 Vehicle Details
      </h2>


      <p
        style={{
          color: "var(--muted-text)",
          marginTop: "8px",
        }}
      >
        Enter the vehicle details to estimate
        its market price.
      </p>


      <form
        onSubmit={handlePredict}
      >


        {/* =================================================
            BRAND
        ================================================== */}

        <SearchableDropdown
          label="Brand"
          options={brands}
          value={formData.brand}
          placeholder="🔍 Search brand..."
          onChange={(value) => {

            setFormData((previous) => ({

              ...previous,

              brand:
                value,

              model:
                "",

              fuel_type:
                "",

              transmission_type:
                "",

              seller_type:
                "",

              engine:
                "",

              max_power:
                "",

              seats:
                "",

            }));


            setModels([]);

            setFuelTypes([]);
            setTransmissions([]);
            setSellerTypes([]);
            setEngines([]);
            setMaxPowers([]);
            setSeats([]);

            setVariants([]);

            setVariantError("");

          }}
        />


        {/* =================================================
            MODEL
        ================================================== */}

        <SearchableDropdown
          label="Model"
          options={models}
          value={formData.model}
          placeholder={
            formData.brand
              ? "🔍 Search model..."
              : "Select brand first"
          }
          disabled={
            !formData.brand
          }
          onChange={(value) => {

            setFormData((previous) => ({

              ...previous,

              model:
                value,

              fuel_type:
                "",

              transmission_type:
                "",

              seller_type:
                "",

              engine:
                "",

              max_power:
                "",

              seats:
                "",

            }));


            setFuelTypes([]);
            setTransmissions([]);
            setSellerTypes([]);
            setEngines([]);
            setMaxPowers([]);
            setSeats([]);

            setVariants([]);

            setVariantError("");

          }}
        />


        {/* =================================================
            FUEL TYPE
        ================================================== */}

        <SearchableDropdown
          label="Fuel Type"
          options={fuelTypes}
          value={formData.fuel_type}
          placeholder={
            formData.model
              ? "🔍 Search fuel type..."
              : "Select model first"
          }
          disabled={
            !formData.model
          }
          onChange={(value) => {

            setFormData((previous) => ({

              ...previous,

              fuel_type:
                value,

            }));

          }}
        />


        {/* =================================================
            TRANSMISSION
        ================================================== */}

        <SearchableDropdown
          label="Transmission"
          options={transmissions}
          value={
            formData.transmission_type
          }
          placeholder={
            formData.model
              ? "🔍 Search transmission..."
              : "Select model first"
          }
          disabled={
            !formData.model
          }
          onChange={(value) => {

            setFormData((previous) => ({

              ...previous,

              transmission_type:
                value,

            }));

          }}
        />


        {/* =================================================
            SELLER TYPE
        ================================================== */}

        <SearchableDropdown
          label="Seller Type"
          options={sellerTypes}
          value={
            formData.seller_type
          }
          placeholder={
            formData.model
              ? "🔍 Search seller type..."
              : "Select model first"
          }
          disabled={
            !formData.model
          }
          onChange={(value) => {

            setFormData((previous) => ({

              ...previous,

              seller_type:
                value,

            }));

          }}
        />


        {/* =================================================
            ENGINE
        ================================================== */}

        <SearchableDropdown
          label="Engine (CC)"
          options={engines}
          value={
            formData.engine
          }
          placeholder={
            formData.model
              ? "🔍 Search engine..."
              : "Select model first"
          }
          disabled={
            !formData.model
          }
          onChange={(value) => {

            setFormData((previous) => ({

              ...previous,

              engine:
                value,

            }));

          }}
        />


        {/* =================================================
            MAX POWER
        ================================================== */}

        <SearchableDropdown
          label="Max Power"
          options={maxPowers}
          value={
            formData.max_power
          }
          placeholder={
            formData.model
              ? "🔍 Search max power..."
              : "Select model first"
          }
          disabled={
            !formData.model
          }
          onChange={(value) => {

            setFormData((previous) => ({

              ...previous,

              max_power:
                value,

            }));

          }}
        />


        {/* =================================================
            SEATS
        ================================================== */}

        <SearchableDropdown
          label="Seats"
          options={seats}
          value={
            formData.seats
          }
          placeholder={
            formData.model
              ? "🔍 Search seats..."
              : "Select model first"
          }
          disabled={
            !formData.model
          }
          onChange={(value) => {

            setFormData((previous) => ({

              ...previous,

              seats:
                value,

            }));

          }}
        />


        {/* =================================================
            VEHICLE AGE
        ================================================== */}

        <div
          style={{
            marginBottom: "24px",
          }}
        >

          <label
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: "8px",
              fontWeight: "600",
            }}
          >

            <span>
              Vehicle Age
            </span>

            <span>
              {Number(
                formData.vehicle_age || 0
              )} years
            </span>

          </label>


          <input
            type="range"
            name="vehicle_age"
            min="0"
            max="20"
            step="1"
            value={
              formData.vehicle_age || 0
            }
            onChange={handleChange}
            style={{
              width: "100%",
              cursor: "pointer",
            }}
          />

        </div>


        {/* =================================================
            KM DRIVEN
        ================================================== */}

        <div
          style={{
            marginBottom: "24px",
          }}
        >

          <label
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: "8px",
              fontWeight: "600",
            }}
          >

            <span>
              KM Driven
            </span>

            <span>
              {Number(
                formData.km_driven || 0
              ).toLocaleString()} km
            </span>

          </label>


          <input
            type="range"
            name="km_driven"
            min="0"
            max="300000"
            step="1000"
            value={
              formData.km_driven || 0
            }
            onChange={handleChange}
            style={{
              width: "100%",
              cursor: "pointer",
            }}
          />

        </div>


        {/* =================================================
            MILEAGE
        ================================================== */}

        <div
          style={{
            marginBottom: "24px",
          }}
        >

          <label
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: "8px",
              fontWeight: "600",
            }}
          >

            <span>
              Mileage
            </span>

            <span>
              {Number(
                formData.mileage || 5
              ).toFixed(1)} km/l
            </span>

          </label>


          <input
            type="range"
            name="mileage"
            min="5"
            max="40"
            step="0.1"
            value={
              formData.mileage || 5
            }
            onChange={handleChange}
            style={{
              width: "100%",
              cursor: "pointer",
            }}
          />

        </div>


        {/* =================================================
            ERROR
        ================================================== */}

        {error && (

          <div
            style={{
                marginTop: "20px",
                padding: "12px",
                borderRadius: "8px",
                background: "var(--danger-bg)",
                color: "#DC2626",
              }}
          >
            {error}
          </div>

        )}


        {/* =================================================
            MAIN BUTTONS
        ================================================== */}

        <div
            style={{
              display: "flex",
              gap: "12px",
              marginTop: "30px",
            }}
        >

          <button
            type="submit"
            disabled={loading}
            style={{
              flex: 1,
              padding: "14px",
              border: "none",
              borderRadius: "8px",
              background:
                loading
                  ? "#9ca3af"
                  : "#2563eb",
              color: "white",
              fontSize: "16px",
              fontWeight: "bold",
              cursor:
                loading
                  ? "not-allowed"
                  : "pointer",
            }}
          >

            {loading
              ? "Predicting..."
              : "🚗 Predict Price"}

          </button>


          <button
            type="button"
            onClick={handleReset}
            style={{
              padding: "14px 22px",
              border:
                "1px solid var(--border)",
              borderRadius: "8px",
              background: "transparent",
              fontSize: "16px",
              color: "var(--text)",
              cursor: "pointer",
            }}
          >

            Reset

          </button>

        </div>


        {/* =================================================
            VARIANT BUTTON
        ================================================== */}

        <div
          style={{
            marginTop: "16px",
          }}
        >

          <button
            type="button"
            onClick={
              handleVariantPrediction
            }
            disabled={
              variantLoading ||
              !formData.brand ||
              !formData.model
            }
            style={{
              width: "100%",
              padding: "14px",
              border: "none",
              borderRadius: "8px",
              background:
                variantLoading ||
                !formData.brand ||
                !formData.model
                  ? "#374151"
                  : "var(--surface)",
              color: "white",
              fontSize: "16px",
              fontWeight: "bold",
              cursor:
                variantLoading ||
                !formData.brand ||
                !formData.model
                  ? "not-allowed"
                  : "pointer",
            }}
          >

            {variantLoading
              ? "Finding Variants..."
              : "🔍 Compare All Variants"}

          </button>

        </div>

      </form>


      {/* =====================================================
          VARIANT ERROR
      ====================================================== */}

      {variantError && (

        <div
          style={{
            marginTop: "20px",
            padding: "12px",
            borderRadius: "8px",
            background: "var(--danger-bg)",
            color: "#DC2626",
          }}
        >

          {variantError}

        </div>

      )}


      {/* =====================================================
          AI SUGGESTIONS
      ====================================================== */}

      {(formData.brand && formData.model && (formData.engine === "" && formData.max_power === "" && formData.seats === "")) && (

        <div
          style={{
            marginTop: "24px",
            padding: "18px",
            borderRadius: "12px",
            background: "var(--card-bg)",
            border: "1px solid var(--card-border)",
          }}
        >

          <h3 style={{ margin: 0 }}>AI Suggestions</h3>

          <p style={{ color: "#6B7280", marginTop: "6px" }}>
            We noticed some missing details. Here are estimated prices for different options.
          </p>

          {suggestionLoading && (
            <div style={{ marginTop: "12px" }}>Loading suggestions...</div>
          )}

          {!suggestionLoading && (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "12px", marginTop: 12 }}>

              {/* Seats */}
              <div style={{ padding: 12, borderRadius: 10, background: "var(--muted-bg)" }}>
                <strong>Seats not provided</strong>
                <div style={{ marginTop: 10 }}>
                  {(suggestions.seats.length === 0) ? (
                    <div style={{ color: '#6B7280', marginTop: 8 }}>Estimated prices for seats will appear after predicting.</div>
                  ) : (
                    suggestions.seats.map((s, idx) => (
                      <div key={`seat-${idx}`} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0" }}>
                        <div>{s.seats} Seats</div>
                        <div>₹ {Number(s.predicted_price).toLocaleString("en-IN", { maximumFractionDigits: 0 })}</div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Engines */}
              <div style={{ padding: 12, borderRadius: 10, background: "var(--muted-bg)" }}>
                <strong>Engine not provided</strong>
                <div style={{ marginTop: 10 }}>
                  {(suggestions.engines.length === 0) ? (
                    <div style={{ color: '#6B7280', marginTop: 8 }}>Estimated prices for engines will appear after predicting.</div>
                  ) : (
                    suggestions.engines.map((e, idx) => (
                      <div key={`eng-${idx}`} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0" }}>
                        <div>{e.engine} CC</div>
                        <div>₹ {Number(e.predicted_price).toLocaleString("en-IN", { maximumFractionDigits: 0 })}</div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Seller types */}
              <div style={{ padding: 12, borderRadius: 10, background: "var(--muted-bg)" }}>
                <strong>Seller Type not provided</strong>
                <div style={{ marginTop: 10 }}>
                  {(suggestions.sellers.length === 0) ? (
                    <div style={{ color: '#6B7280', marginTop: 8 }}>Estimated prices for seller types will appear after predicting.</div>
                  ) : (
                    suggestions.sellers.map((s, idx) => (
                      <div key={`sell-${idx}`} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0" }}>
                        <div>{s.seller_type}</div>
                        <div>₹ {Number(s.predicted_price).toLocaleString("en-IN", { maximumFractionDigits: 0 })}</div>
                      </div>
                    ))
                  )}
                </div>
              </div>

            </div>

          )}

        </div>

      )}


      {/* =====================================================
          VARIANT RESULTS
      ====================================================== */}

      {variants.length > 0 && (

        <div
          style={{
            marginTop: "30px",
          }}
        >

          {/* -------------------------------------------------
              Header
          -------------------------------------------------- */}

          <div
            style={{
              display: "flex",
              justifyContent:
                "space-between",
              alignItems: "center",
              marginBottom: "16px",
            }}
          >

            <div>

              <h3
                style={{
                  margin: 0,
                }}
              >
                🚘 Variant Comparison
              </h3>


              <p
                style={{
                  marginTop: "5px",
                  color: "#6B7280",
                }}
              >
                {variants.length} variants found
              </p>

            </div>

          </div>


          {/* -------------------------------------------------
              Variant cards
          -------------------------------------------------- */}

          <div
            style={{
              display: "grid",
              gap: "14px",
            }}
          >

            {variants.map(
              (variant, index) => {

                const variantName =
                  variant.variant ||
                  variant.name ||
                  "Unknown Variant";


                const predictedPrice =
                  variant.predicted_price ??
                  variant.price ??
                  0;


                return (

                  <div
                    key={
                      `${variantName}-${index}`
                    }
                    style={{
                      padding: "18px",
                      border:
                        index === 0
                          ? "2px solid var(--primary)"
                          : "1px solid var(--card-border)",
                      borderRadius: "12px",
                      background: "var(--card-bg)",
                      boxShadow:
                        "0 8px 20px rgba(0,0,0,0.06)",
                    }}
                  >

                    {/* =====================================
                        Variant title + price
                    ====================================== */}

                    <div
                      style={{
                        display: "flex",
                        justifyContent:
                          "space-between",
                        gap: "15px",
                        alignItems:
                          "center",
                      }}
                    >

                      <div>

                        <h4
                          style={{
                            margin: 0,
                            fontSize: "17px",
                          }}
                        >
                          {variantName}
                        </h4>


                          {index === 0 && (

                          <span
                            style={{
                              display:
                                "inline-block",
                              marginTop:
                                "6px",
                              padding:
                                "4px 8px",
                              borderRadius:
                                "6px",
                              background:
                                "rgba(37,99,235,0.12)",
                              color:
                                "var(--primary)",
                              fontSize:
                                "12px",
                              fontWeight:
                                "600",
                            }}
                          >
                            Highest Predicted Price
                          </span>

                        )}

                      </div>


                      <div
                        style={{
                          fontSize: "20px",
                          fontWeight: "bold",
                          whiteSpace:
                            "nowrap",
                        }}
                      >

                        ₹{" "}

                        {Number(
                          predictedPrice
                        ).toLocaleString(
                          "en-IN"
                        )}

                      </div>

                    </div>


                    {/* =====================================
                        Specification badges
                    ====================================== */}

                    <div
                      style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "8px",
                        marginTop: "14px",
                      }}
                    >

                      {variant.fuel_type && (

                        <span
                          style={{
                            padding:
                              "5px 9px",
                            borderRadius:
                              "6px",
                            background:
                              "var(--muted-bg)",
                            fontSize:
                              "13px",
                            color: "var(--text)",
                          }}
                        >
                          ⛽{" "}
                          {variant.fuel_type}
                        </span>

                      )}


                      {variant.transmission_type && (

                        <span
                          style={{
                            padding:
                              "5px 9px",
                            borderRadius:
                              "6px",
                            background:
                              "var(--muted-bg)",
                            fontSize:
                              "13px",
                            color: "var(--text)",
                          }}
                        >
                          ⚙️{" "}
                          {
                            variant.transmission_type
                          }
                        </span>

                      )}


                      {variant.seats !== undefined &&
                        variant.seats !== null && (

                          <span
                            style={{
                              padding:
                                "5px 9px",
                              borderRadius:
                                "6px",
                              background:
                                "var(--muted-bg)",
                              fontSize:
                                "13px",
                              color: "var(--text)",
                            }}
                          >
                            🪑{" "}
                            {variant.seats} seats
                          </span>

                        )}


                      {variant.max_power !== undefined &&
                        variant.max_power !== null && (

                          <span
                            style={{
                              padding:
                                "5px 9px",
                              borderRadius:
                                "6px",
                              background:
                                "var(--muted-bg)",
                              fontSize:
                                "13px",
                              color: "var(--text)",
                            }}
                          >
                            ⚡{" "}
                            {variant.max_power} HP
                          </span>

                        )}

                    </div>


                    {/* =====================================
                        Engine
                    ====================================== */}

                    {variant.engine_type && (

                      <div
                        style={{
                          marginTop: "10px",
                          color: "#6B7280",
                          fontSize: "13px",
                        }}
                      >
                        Engine:{" "}
                        {variant.engine_type}
                      </div>

                    )}

                  </div>

                );

              }
            )}

          </div>

        </div>

      )}


      {/* =====================================================
          NORMAL PREDICTION RESULT
      ====================================================== */}

      {prediction && (

        <div
          style={{
            marginTop: "30px",
            padding: "24px",
            borderRadius: "12px",
            background: "#f3f4f6",
            textAlign: "center",
          }}
        >

          <h3>
            💰 Predicted Price
          </h3>


          <p
            style={{
              marginTop: "10px",
              fontSize: "32px",
              fontWeight: "bold",
            }}
          >

            ₹{" "}

            {Number(
              prediction.predicted_price
            ).toLocaleString(
              "en-IN"
            )}

          </p>


          <p
            style={{
              color: "#6B7280",
              marginTop: "5px",
            }}
          >

            Estimated Market Price

          </p>


          {/* =================================================
              PRICE RANGE
          ================================================== */}

          {prediction.price_range && (

            <div
              style={{
                marginTop: "18px",
                display: "flex",
                justifyContent:
                  "center",
                gap: "30px",
                flexWrap: "wrap",
              }}
            >

              <div>

                <div
                  style={{
                    fontSize: "12px",
                    color: "#6B7280",
                  }}
                >
                  Low
                </div>

                <strong>
                  ₹{" "}
                  {Number(
                    prediction.price_range.low
                  ).toLocaleString(
                    "en-IN"
                  )}
                </strong>

              </div>


              <div>

                <div
                  style={{
                    fontSize: "12px",
                    color: "#6B7280",
                  }}
                >
                  Predicted
                </div>

                <strong>
                  ₹{" "}
                  {Number(
                    prediction.price_range.predicted
                  ).toLocaleString(
                    "en-IN"
                  )}
                </strong>

              </div>


              <div>

                <div
                  style={{
                    fontSize: "12px",
                    color: "#6B7280",
                  }}
                >
                  High
                </div>

                <strong>
                  ₹{" "}
                  {Number(
                    prediction.price_range.high
                  ).toLocaleString(
                    "en-IN"
                  )}
                </strong>

              </div>

            </div>

          )}

        </div>

      )}

    </div>

  );

}


export default CarForm;