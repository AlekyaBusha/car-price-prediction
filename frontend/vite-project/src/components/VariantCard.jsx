/**
 * VariantCard.jsx
 * Individual vehicle variant card component displaying real variant names,
 * contained responsive prices, and full vehicle specifications.
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
    if (value === null || value === undefined || value === "") return "-";
    if (typeof value === "number") {
      return Number.isInteger(value) ? value.toString() : value.toFixed(1);
    }
    return value.toString();
  };

  // Real variant name display
  const variantTitle = variant.variant
    ? String(variant.variant).toUpperCase()
    : variant.model
    ? `${variant.model} Variant`
    : `Variant ${index}`;

  const confidencePct = variant.confidence
    ? Math.round(variant.confidence * 100)
    : 95;

  return (
    <div className={`variant-card ${isHighest ? "highest" : ""}`}>
      <div className="variant-header">
        <div className="variant-header-left">
          <h4 className="variant-title" title={variantTitle}>
            {variantTitle}
          </h4>
          <p className="variant-subtitle">
            {formatValue(variant.fuel_type)} • {formatValue(variant.transmission_type)}
          </p>
          {isHighest && <div className="highest-badge">Top Variant</div>}
        </div>
        <div className="variant-price-box">
          <span className="variant-price-label">Predicted Price</span>
          <span className="variant-price">
            {formatPrice(variant.predicted_price)}
          </span>
        </div>
      </div>

      <div className="variant-specs">
        <div className="spec-row">
          <span className="spec-label">Fuel Type</span>
          <span className="spec-value">{formatValue(variant.fuel_type)}</span>
        </div>

        <div className="spec-row">
          <span className="spec-label">Transmission</span>
          <span className="spec-value">{formatValue(variant.transmission_type)}</span>
        </div>

        <div className="spec-row">
          <span className="spec-label">Engine</span>
          <span className="spec-value">
            {variant.engine ? `${formatValue(variant.engine)} CC` : formatValue(variant.engine_type || "-")}
          </span>
        </div>

        <div className="spec-row">
          <span className="spec-label">Max Power</span>
          <span className="spec-value">
            {variant.max_power ? `${formatValue(variant.max_power)} bhp` : "-"}
          </span>
        </div>

        <div className="spec-row">
          <span className="spec-label">Seats</span>
          <span className="spec-value">{formatValue(variant.seats)} Seats</span>
        </div>

        <div className="spec-row">
          <span className="spec-label">Mileage</span>
          <span className="spec-value">{formatValue(variant.mileage)} km/l</span>
        </div>
      </div>

      <div className="variant-confidence">
        <div className="confidence-header">
          <span className="confidence-label">Confidence</span>
          <span className="confidence-value">{confidencePct}%</span>
        </div>
        <div className="confidence-track">
          <div
            className="confidence-fill"
            style={{ width: `${Math.min(100, Math.max(10, confidencePct))}%` }}
          />
        </div>
      </div>
    </div>
  );
}
