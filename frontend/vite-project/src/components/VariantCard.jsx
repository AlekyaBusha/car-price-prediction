/**
 * VariantCard.jsx
 * Individual variant card component
 */

import "../styles/VariantCard.css";

export default function VariantCard({ variant, index, isHighest = false }) {
  const formatPrice = (price) => {
    if (!price && price !== 0) return "N/A";
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(price);
  };

  const formatValue = (value) => {
    if (value === null || value === undefined) return "-";
    if (typeof value === "number") {
      return Number.isInteger(value)
        ? value.toString()
        : value.toFixed(1);
    }
    return value.toString();
  };

  return (
    <div className={`variant-card ${isHighest ? "highest" : ""}`}>
      <div className="variant-header">
        <div>
          <h4 className="variant-title">{variant.model || `Variant ${index}`}</h4>
          <p className="variant-subtitle">
            {formatValue(variant.fuel_type)} | {formatValue(variant.transmission_type)}
          </p>
          {isHighest && <div className="highest-badge">Highest Predicted Price</div>}
        </div>
        <div className="variant-price">
          {formatPrice(variant.predicted_price)}
        </div>
      </div>

      <div className="variant-specs">
        <div className="spec-row">
          <span className="spec-label">Fuel Type</span>
          <span className="spec-value">
            {formatValue(variant.fuel_type)}
          </span>
        </div>

        <div className="spec-row">
          <span className="spec-label">Transmission</span>
          <span className="spec-value">
            {formatValue(variant.transmission_type)}
          </span>
        </div>

        <div className="spec-row">
          <span className="spec-label">Seats</span>
          <span className="spec-value">
            {formatValue(variant.seats)}
          </span>
        </div>

        <div className="spec-row">
          <span className="spec-label">Max Power</span>
          <span className="spec-value">
            {formatValue(variant.max_power)} bhp
          </span>
        </div>
      </div>

      <div className="engine-type-label">Engine Type</div>
      <div className="engine-type-value">
        {formatValue(variant.engine)} CC - {formatValue(variant.engine_type || "N/A")}
      </div>
    </div>
  );
}
