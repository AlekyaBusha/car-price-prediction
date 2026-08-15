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
  explainPrice,
  forecastPrice,
} from "../services/api";

import SearchableDropdown from "./SearchableDropdown";


function CarForm({ onPrediction }) {

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
    vehicle_age: "",
    km_driven: "",
    mileage: "",
  });


  // =========================================================
  // Result state
  // =========================================================

  const [prediction, setPrediction] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


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
  // Load all options based on Brand + Model
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
          brand: formData.brand,
          model: formData.model,

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
  // Prediction
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
      !formData.seller_type ||
      !formData.vehicle_age ||
      !formData.km_driven
    ) {

      setError(
        "Please fill Brand, Model, Fuel Type, Transmission, Seller Type, Vehicle Age and KM Driven."
      );

      return;

    }


    try {

      setLoading(true);


      // =====================================================
      // ONE COMMON PAYLOAD
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


        engine:
          formData.engine !== ""
            ? Number(formData.engine)
            : null,


        max_power:
          formData.max_power !== ""
            ? Number(formData.max_power)
            : null,


        seats:
          formData.seats !== ""
            ? Number(formData.seats)
            : null,


        vehicle_age:
          formData.vehicle_age !== ""
            ? Number(formData.vehicle_age)
            : null,


        km_driven:
          formData.km_driven !== ""
            ? Number(formData.km_driven)
            : null,


        mileage:
          formData.mileage !== ""
            ? Number(formData.mileage)
            : null,

      };


      console.log(
        "================================="
      );

      console.log(
        "Sending prediction request:"
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

        console.log(
          "Sending SHAP request:"
        );

        console.log(payload);


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

        explanation = null;

      }


      // =====================================================
      // Forecast
      // =====================================================

      let forecast = [];


      try {

        console.log(
          "Sending forecast request:"
        );

        console.log(payload);


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

        forecast = [];

      }


      // =====================================================
      // Check prediction vs SHAP
      // =====================================================

      if (
        explanation &&
        explanation.prediction !== undefined
      ) {

        console.log(
          "Prediction price:"
        );

        console.log(
          result.predicted_price
        );


        console.log(
          "SHAP prediction:"
        );

        console.log(
          explanation.prediction
        );


        console.log(
          "SHAP difference:"
        );

        console.log(
          Number(
            explanation.prediction
          ) -
          Number(
            result.predicted_price
          )
        );

      }


      // =====================================================
      // Check prediction vs forecast
      // =====================================================

      if (
        forecast &&
        forecast.length > 0
      ) {

        const currentForecast =
          forecast.find(
            (item) =>
              Number(item.months) === 0
          );


        if (currentForecast) {

          console.log(
            "Current prediction:"
          );

          console.log(
            result.predicted_price
          );


          console.log(
            "Forecast month 0:"
          );

          console.log(
            currentForecast.price
          );


          console.log(
            "Difference between prediction and forecast:"
          );

          console.log(
            Number(
              currentForecast.price
            ) -
            Number(
              result.predicted_price
            )
          );

        }

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


      console.log(
        "Final dashboard result:"
      );

      console.log(
        finalResult
      );


      setPrediction(
        finalResult
      );


      // Send result to Dashboard
      if (onPrediction) {

        onPrediction(
          finalResult
        );

      }

    } catch (err) {

      console.error(
        "Prediction error:",
        err
      );


      setError(
        err.message ||
        "Failed to predict car price."
      );

    } finally {

      setLoading(false);

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
      vehicle_age: "",
      km_driven: "",
      mileage: "",

    });


    setModels([]);

    setFuelTypes([]);
    setTransmissions([]);
    setSellerTypes([]);
    setEngines([]);
    setMaxPowers([]);
    setSeats([]);

    setPrediction(null);

    setError("");

  }


  // =========================================================
  // UI
  // =========================================================

  return (

    <div
      style={{
        background: "white",
        padding: "40px",
        borderRadius: "16px",
        boxShadow:
          "0 6px 20px rgba(0,0,0,.08)",
      }}
    >

      <h2>
        🚘 Vehicle Details
      </h2>


      <p
        style={{
          color: "#666",
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
        ================================================= */}

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
        ================================================= */}

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
        ================================================= */}

        <div
          style={{
            marginTop: "20px",
          }}
        >

          <label>

            <strong>
              Vehicle Age (Years)
            </strong>

          </label>


          <input
            type="number"
            name="vehicle_age"
            value={
              formData.vehicle_age
            }
            onChange={
              handleChange
            }
            min="0"
            step="0.1"
            placeholder="Example: 5"
            style={{
              marginTop: "8px",
              width: "100%",
              padding: "12px",
              boxSizing: "border-box",
              border:
                "1px solid #d1d5db",
              borderRadius: "8px",
              fontSize: "15px",
            }}
          />

        </div>


        {/* =================================================
            KM DRIVEN
        ================================================== */}

        <div
          style={{
            marginTop: "20px",
          }}
        >

          <label>

            <strong>
              KM Driven
            </strong>

          </label>


          <input
            type="number"
            name="km_driven"
            value={
              formData.km_driven
            }
            onChange={
              handleChange
            }
            min="0"
            placeholder="Example: 45000"
            style={{
              marginTop: "8px",
              width: "100%",
              padding: "12px",
              boxSizing: "border-box",
              border:
                "1px solid #d1d5db",
              borderRadius: "8px",
              fontSize: "15px",
            }}
          />

        </div>


        {/* =================================================
            MILEAGE
        ================================================== */}

        <div
          style={{
            marginTop: "20px",
          }}
        >

          <label>

            <strong>
              Mileage (km/l)
            </strong>

          </label>


          <input
            type="number"
            name="mileage"
            value={
              formData.mileage
            }
            onChange={
              handleChange
            }
            min="0"
            step="0.1"
            placeholder="Example: 18"
            style={{
              marginTop: "8px",
              width: "100%",
              padding: "12px",
              boxSizing: "border-box",
              border:
                "1px solid #d1d5db",
              borderRadius: "8px",
              fontSize: "15px",
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
              background:
                "#fee2e2",
              color:
                "#b91c1c",
            }}
          >

            {error}

          </div>

        )}


        {/* =================================================
            BUTTONS
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
            onClick={
              handleReset
            }
            style={{
              padding:
                "14px 22px",
              border:
                "1px solid #d1d5db",
              borderRadius: "8px",
              background:
                "white",
              fontSize: "16px",
              cursor:
                "pointer",
            }}
          >

            Reset

          </button>

        </div>

      </form>


      {/* =====================================================
          LOCAL PREDICTION
          Dashboard also receives the same result through
          onPrediction().
      ====================================================== */}

      {prediction && (

        <div
          style={{
            marginTop: "30px",
            padding: "24px",
            borderRadius: "12px",
            background:
              "#f3f4f6",
            textAlign:
              "center",
          }}
        >

          <h3>
            💰 Predicted Price
          </h3>


          <p
            style={{
              marginTop: "10px",
              fontSize: "32px",
              fontWeight:
                "bold",
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
              color: "#666",
              marginTop: "5px",
            }}
          >
            Estimated Market Price
          </p>

        </div>

      )}

    </div>

  );

}


export default CarForm;