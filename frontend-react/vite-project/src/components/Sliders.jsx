import React from "react";

function Sliders({
  vehicleAge,
  setVehicleAge,
  kmDriven,
  setKmDriven,
  mileage,
  setMileage,
}) {
  return (
    <div className="sliders">

      {/* Vehicle Age */}
      <div className="slider-group">
        <div className="slider-header">
          <label>Vehicle Age</label>
          <strong>{vehicleAge} years</strong>
        </div>

        <input
          type="range"
          min="0"
          max="20"
          step="0.5"
          value={vehicleAge}
          onChange={(e) =>
            setVehicleAge(Number(e.target.value))
          }
        />
      </div>


      {/* Kilometres Driven */}
      <div className="slider-group">
        <div className="slider-header">
          <label>KM Driven</label>
          <strong>
            {Number(kmDriven).toLocaleString()} km
          </strong>
        </div>

        <input
          type="range"
          min="0"
          max="300000"
          step="1000"
          value={kmDriven}
          onChange={(e) =>
            setKmDriven(Number(e.target.value))
          }
        />
      </div>


      {/* Mileage */}
      <div className="slider-group">
        <div className="slider-header">
          <label>Mileage</label>
          <strong>{mileage} km/l</strong>
        </div>

        <input
          type="range"
          min="5"
          max="40"
          step="0.5"
          value={mileage}
          onChange={(e) =>
            setMileage(Number(e.target.value))
          }
        />
      </div>

    </div>
  );
}

export default Sliders;