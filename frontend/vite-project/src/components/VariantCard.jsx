/**
 * VariantCard.jsx
 * Individual variant card component
 */

import "../styles/VariantCard.css";

export default function VariantCard({ variant, index }) {
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
    <div className="variant-card">
      <div className="variant-header">
        <div>
          <h4 className="variant-title">Variant {index}</h4>
          <p className="variant-subtitle">
            {formatValue(variant.fuel_type)} | {formatValue(variant.transmission_type)}
          </p>
        </div>
        <div className="variant-price">
          {formatPrice(variant.predicted_price)}
        </div>
      </div>

      <div className="variant-specs">
        <div className="spec-row">
          <span className="spec-label">Engine</span>
          <span className="spec-value">
            {formatValue(variant.engine)} CC
          </span>
        </div>

        <div className="spec-row">
          <span className="spec-label">Power</span>
          <span className="spec-value">
            {formatValue(variant.max_power)} bhp
          </span>
        </div>

        <div className="spec-row">
          <span className="spec-label">Seats</span>
          <span className="spec-value">
            {formatValue(variant.seats)}
          </span>
        </div>

        <div className="spec-row">
          <span className="spec-label">Mileage</span>
          <span className="spec-value">
            {formatValue(variant.mileage)} km/l
          </span>
        </div>
      </div>

      <div className="variant-confidence">
        <div className="confidence-label">Prediction Confidence</div>
        <div className="confidence-bar">
          <div
            className="confidence-fill"
            style={{
              width: `${Math.min(
                Math.max(
                  (variant.confidence_score || 0.8) * 100,
                  0
                ),
                100
              )}%`,
            }}
          ></div>
        </div>
        <div className="confidence-text">
          {Math.round((variant.confidence_score || 0.8) * 100)}% confident
        </div>
      </div>
    </div>
  );
}
