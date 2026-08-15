import React from "react";

function InputForm({
  formData,
  setFormData,
}) {
  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  return (
    <div className="input-form">

      <div className="form-grid">

        {/* Brand */}
        <div className="form-field">
          <label>
            Brand <span>*</span>
          </label>

          <input
            type="text"
            name="brand"
            value={formData.brand}
            onChange={handleChange}
            placeholder="Enter brand"
          />
        </div>


        {/* Model */}
        <div className="form-field">
          <label>
            Model <span>*</span>
          </label>

          <input
            type="text"
            name="model"
            value={formData.model}
            onChange={handleChange}
            placeholder="Enter model"
          />
        </div>


        {/* Fuel Type */}
        <div className="form-field">
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
        <div className="form-field">
          <label>
            Transmission <span>*</span>
          </label>

          <select
            name="transmission_type"
            value={formData.transmission_type}
            onChange={handleChange}
          >
            <option value="">
              Select transmission
            </option>

            <option value="Manual">Manual</option>
            <option value="Automatic">Automatic</option>
          </select>
        </div>


        {/* Seller Type */}
        <div className="form-field">
          <label>Seller Type</label>

          <select
            name="seller_type"
            value={formData.seller_type}
            onChange={handleChange}
          >
            <option value="">
              Select seller type
            </option>

            <option value="Individual">
              Individual
            </option>

            <option value="Dealer">
              Dealer
            </option>

            <option value="Trustmark Dealer">
              Trustmark Dealer
            </option>
          </select>
        </div>


        {/* Engine */}
        <div className="form-field">
          <label>Engine (CC)</label>

          <input
            type="number"
            name="engine"
            value={formData.engine}
            onChange={handleChange}
            placeholder="e.g. 1197"
          />
        </div>


        {/* Max Power */}
        <div className="form-field">
          <label>Max Power (bhp)</label>

          <input
            type="number"
            name="max_power"
            value={formData.max_power}
            onChange={handleChange}
            placeholder="e.g. 82"
          />
        </div>


        {/* Seats */}
        <div className="form-field">
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
            <option value="9">9</option>
          </select>
        </div>

      </div>

    </div>
  );
}

export default InputForm;