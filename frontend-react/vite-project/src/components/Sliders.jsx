function Sliders({ carDetails, onChange }) {
  return (
    <div className="grid-2" style={{ marginTop: "1rem" }}>
      <div className="field">
        <label>Vehicle Age (years): {carDetails.vehicle_age}</label>
        <input type="range" min="0" max="25" value={carDetails.vehicle_age}
          onChange={e => onChange("vehicle_age", parseInt(e.target.value))} />
      </div>
      <div className="field">
        <label>Kilometers Driven: {carDetails.km_driven.toLocaleString()}</label>
        <input type="range" min="0" max="300000" step="5000" value={carDetails.km_driven}
          onChange={e => onChange("km_driven", parseInt(e.target.value))} />
      </div>
    </div>
  )
}

export default Sliders