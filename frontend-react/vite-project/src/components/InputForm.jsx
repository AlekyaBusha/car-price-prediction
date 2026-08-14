function InputForm({ carDetails, onChange }) {
  return (
    <section>
      <h2 className="section-header">Car Details</h2>
      <div className="grid-3">
        <div className="field">
          <label>Brand</label>
          <select value={carDetails.brand} onChange={e => onChange("brand", e.target.value)}>
            {["Maruti", "Hyundai", "Honda", "Mahindra", "Toyota", "Ford",
              "Volkswagen", "Renault", "Tata", "BMW", "Skoda", "Mercedes-Benz",
              "Audi", "Datsun", "Jaguar", "Other"].map(b => <option key={b} value={b}>{b}</option>)}
          </select>
        </div>

        <div className="field">
          <label>Fuel Type</label>
          <select value={carDetails.fuel_type} onChange={e => onChange("fuel_type", e.target.value)}>
            {["Petrol", "Diesel", "CNG", "LPG", "Electric"].map(f => <option key={f} value={f}>{f}</option>)}
          </select>
        </div>

        <div className="field">
          <label>Mileage (kmpl)</label>
          <input type="number" value={carDetails.mileage}
            onChange={e => onChange("mileage", parseFloat(e.target.value))} />
        </div>

        <div className="field">
          <label>Model</label>
          <input type="text" value={carDetails.model}
            onChange={e => onChange("model", e.target.value)} />
        </div>

        <div className="field">
          <label>Transmission</label>
          <select value={carDetails.transmission_type} onChange={e => onChange("transmission_type", e.target.value)}>
            {["Manual", "Automatic"].map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>

        <div className="field">
          <label>Engine (CC)</label>
          <input type="number" value={carDetails.engine}
            onChange={e => onChange("engine", parseInt(e.target.value))} />
        </div>

        <div className="field">
          <label>Seller Type</label>
          <select value={carDetails.seller_type} onChange={e => onChange("seller_type", e.target.value)}>
            {["Individual", "Dealer", "Trustmark Dealer"].map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>

        <div className="field">
          <label>Seats</label>
          <select value={carDetails.seats} onChange={e => onChange("seats", parseInt(e.target.value))}>
            {[2, 4, 5, 6, 7, 8].map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>

        <div className="field">
          <label>Max Power (bhp)</label>
          <input type="number" value={carDetails.max_power}
            onChange={e => onChange("max_power", parseFloat(e.target.value))} />
        </div>
      </div>
    </section>
  )
}

export default InputForm
