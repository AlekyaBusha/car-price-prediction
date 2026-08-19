/**
 * PriceRange.jsx
 * Display low, predicted, and high price range
 */

import "../styles/PriceRange.css";

export default function PriceRange({ data, predictionMode, message }) {
  if (!data) {
    return null;
  }

  const { low, predicted, high } = data;

  const formatPrice = (price) => {
    if (!price && price !== 0) return "N/A";
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(price);
  };

  const priceRange = high - low;
  const lowPercentage = low && priceRange > 0 ? ((predicted - low) / priceRange) * 100 : 50;

  return (
    <div className="price-range-container">
      <h3 className="section-title">Price Range</h3>

      <div className="price-range-display">
        {/* Predicted Price (Large) */}
        <div className="predicted-price-box">
          <p className="label">Predicted Selling Price</p>
          <p className="predicted-value">{formatPrice(predicted)}</p>
        </div>

        {/* Fallback mode informational notice */}
        {message && (
          <div className="fallback-info-badge">
            <span className="fallback-info-icon">ℹ️</span>
            <div className="fallback-info-content">
              <p className="fallback-info-title">Vehicle configuration estimated with XGBoost</p>
              <p className="fallback-info-text">{message}</p>
            </div>
          </div>
        )}

        {/* Price Range Visualization */}
        <div className="range-visualization">
          <div className="range-labels">
            <span className="low-label">{formatPrice(low)}</span>
            <span className="high-label">{formatPrice(high)}</span>
          </div>

          <div className="range-bar">
            <div
              className="range-marker"
              style={{ left: `${Math.max(0, Math.min(100, lowPercentage))}%` }}
              title={`Predicted: ${formatPrice(predicted)}`}
            ></div>
          </div>

          <div className="range-info">
            <p className="info-text">
              Price likely to range between{" "}
              <strong>{formatPrice(low)}</strong> and{" "}
              <strong>{formatPrice(high)}</strong>
            </p>
          </div>
        </div>

        {/* Price Breakdown Grid */}
        <div className="price-grid">
          <div className="price-item">
            <span className="label">Low Estimate</span>
            <span className="value">{formatPrice(low)}</span>
          </div>
          <div className="price-item">
            <span className="label">Market Price</span>
            <span className="value">{formatPrice(predicted)}</span>
          </div>
          <div className="price-item">
            <span className="label">High Estimate</span>
            <span className="value">{formatPrice(high)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
