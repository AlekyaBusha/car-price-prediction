import { useEffect, useState } from "react";
import { getBrands, getModels } from "../services/api";

function CarForm({ onPredict, loading }) {
  const [brands, setBrands] = useState([]);
  const [models, setModels] = useState([]);

  const [formData, setFormData] = useState({
    brand: "",
    model: "",
    fuel_type: "",
    transmission_type: "",
    engine: "",
    seller_type: "",
    seats: "",
    max_power: "",
    vehicle_age: "",
    km_driven: "",
    mileage: "",
  });

  const [error, setError] = useState("");

  // Load brands from backend
  useEffect(() => {
    async function loadBrands() {
      try {
        const result = await getBrands();

        const brandList =
          result?.data?.brands ||
          result?.brands ||
          [];

        setBrands(brandList);
      } catch (err) {
        console.error("Failed to load brands:", err);
      }
    }

    loadBrands();
  }, []);

  // Load models whenever brand changes
  useEffect(() => {
    async function loadModels() {
      if (!formData.brand) {
        setModels([]);
        return;
      }

      try {
        const result = await getModels(formData.brand);

        const modelList =
          result?.data?.models ||
          result?.models ||
          [];

        setModels(modelList);
      } catch (err) {
        console.error("Failed to load models:", err);
        setModels([]);
      }
    }

    loadModels();
  }, [formData.brand]);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    setError("");
  }

  function handleBrandChange(event) {
    const value = event.target.value;

    setFormData((previous) => ({
      ...previous,
      brand: value,
      model: "",
    }));

    setError("");
  }

  function handleSubmit(event) {
    event.preventDefault();

    if (
      !formData.brand ||
      !formData.model ||
      !formData.fuel_type ||
      !formData.transmission_type
    ) {
      setError("Please fill all required fields.");
      return;
    }

    const payload = {
      brand: formData.brand,
      model: formData.model,
      fuel_type: formData.fuel_type,
      transmission_type: formData.transmission_type,

      ...(formData.seller_type && {
        seller_type: formData.seller_type,
      }),

      ...(formData.engine && {
        engine: Number(formData.engine),
      }),

      ...(formData.max_power && {
        max_power: Number(formData.max_power),
      }),

      ...(formData.seats && {
        seats: Number(formData.seats),
      }),

      ...(formData.vehicle_age && {
        vehicle_age: Number(formData.vehicle_age),
      }),

      ...(formData.km_driven && {
        km_driven: Number(formData.km_driven),
      }),

      ...(formData.mileage && {
        mileage: Number(formData.mileage),
      }),
    };

    onPredict(payload);
  }

  function handleReset() {
    setFormData({
      brand: "",
      model: "",
      fuel_type: "",
      transmission_type: "",
      engine: "",
      seller_type: "",
      seats: "",
      max_power: "",
      vehicle_age: "",
      km_driven: "",
      mileage: "",
    });

    setModels([]);
    setError("");
  }

  return (
    <section className="vehicle-card">
      <div className="section-heading">
        <div className="section-icon blue-icon">🚗</div>

        <div>
          <h2>Vehicle Details</h2>
          <p>Enter your car details to get accurate price prediction</p>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-grid">

          {/* Brand */}
          <div className="form-group">
            <label>
              Brand <span>*</span>
            </label>

            <select
              name="brand"
              value={formData.brand}
              onChange={handleBrandChange}
            >
              <option value="">Search brand...</option>

              {brands.map((brand) => (
                <option key={brand} value={brand}>
                  {brand}
                </option>
              ))}
            </select>
          </div>

          {/* Model */}
          <div className="form-group">
            <label>
              Model <span>*</span>
            </label>

            <select
              name="model"
              value={formData.model}
              onChange={handleChange}
              disabled={!formData.brand}
            >
              <option value="">Search model...</option>

              {models.map((model) => (
                <option key={model} value={model}>
                  {model}
                </option>
              ))}
            </select>
          </div>

          {/* Fuel */}
          <div className="form-group">
            <label>
              Fuel Type <span>*</span>
            </label>

            <select
              name="fuel_type"
              value={formData.fuel_type}
              onChange={handleChange}
            >
              <option value="">Select fuel type</option>
              <option value="Petrol">Petrol</option>
              <option value="Diesel">Diesel</option>
              <option value="CNG">CNG</option>
              <option value="LPG">LPG</option>
              <option value="Electric">Electric</option>
            </select>
          </div>

          {/* Transmission */}
          <div className="form-group">
            <label>
              Transmission <span>*</span>
            </label>

            <select
              name="transmission_type"
              value={formData.transmission_type}
              onChange={handleChange}
            >
              <option value="">Select transmission</option>
              <option value="Manual">Manual</option>
              <option value="Automatic">Automatic</option>
            </select>
          </div>

          {/* Engine */}
          <div className="form-group">
            <label>Engine</label>

            <input
              type="number"
              name="engine"
              value={formData.engine}
              onChange={handleChange}
              placeholder="Engine CC"
            />
          </div>

          {/* Seller */}
          <div className="form-group">
            <label>Seller Type</label>

            <select
              name="seller_type"
              value={formData.seller_type}
              onChange={handleChange}
            >
              <option value="">Select seller type</option>
              <option value="Individual">Individual</option>
              <option value="Dealer">Dealer</option>
              <option value="Trustmark Dealer">
                Trustmark Dealer
              </option>
            </select>
          </div>

          {/* Seats */}
          <div className="form-group">
            <label>Seats</label>

            <select
              name="seats"
              value={formData.seats}
              onChange={handleChange}
            >
              <option value="">Select seats</option>
              <option value="2">2</option>
              <option value="4">4</option>
              <option value="5">5</option>
              <option value="6">6</option>
              <option value="7">7</option>
              <option value="8">8</option>
            </select>
          </div>

          {/* Max Power */}
          <div className="form-group">
            <label>Max Power</label>

            <input
              type="number"
              name="max_power"
              value={formData.max_power}
              onChange={handleChange}
              placeholder="Max power"
            />
          </div>

          {/* Vehicle Age */}
          <div className="form-group">
            <label>Vehicle Age</label>

            <input
              type="number"
              name="vehicle_age"
              value={formData.vehicle_age}
              onChange={handleChange}
              placeholder="Years"
              min="0"
            />
          </div>

          {/* KM Driven */}
          <div className="form-group">
            <label>KM Driven</label>

            <input
              type="number"
              name="km_driven"
              value={formData.km_driven}
              onChange={handleChange}
              placeholder="Kilometres"
              min="0"
            />
          </div>

          {/* Mileage */}
          <div className="form-group">
            <label>Mileage</label>

            <input
              type="number"
              name="mileage"
              value={formData.mileage}
              onChange={handleChange}
              placeholder="km/l"
              step="0.1"
              min="0"
            />
          </div>

        </div>

        {error && (
          <div className="form-error">
            {error}
          </div>
        )}

        <div className="form-actions">
          <button
            type="button"
            className="reset-button"
            onClick={handleReset}
          >
            ↻ Reset
          </button>

          <button
            type="submit"
            className="predict-button"
            disabled={loading}
          >
            {loading ? "Predicting..." : "🚀 Predict Price"}
          </button>
        </div>
      </form>
    </section>
  );
}

export default CarForm;