/**
 * ShapExplanation.jsx
 * Display SHAP feature importance explanation
 */

import "../styles/ShapExplanation.css";

export default function ShapExplanation({ explanation, loading }) {
  if (loading) {
    return (
      <div className="shap-container">
        <p className="loading-text">Loading explanation...</p>
      </div>
    );
  }

  if (
    !explanation ||
    !explanation.top_features ||
    explanation.top_features.length === 0
  ) {
    return (
      <div className="shap-container">
        <p className="no-data-message">No explanation data available.</p>
      </div>
    );
  }

  const { top_features } = explanation;

  // Find max absolute value for scaling
  const maxAbsValue = Math.max(
    ...top_features.map((f) => Math.abs(f.impact || 0))
  );

  return (
    <div className="shap-container">
      <h3 className="section-title">Feature Importance (SHAP)</h3>

      <p className="shap-description">
        These are the most important factors influencing the predicted price.
        Positive values increase the price, negative values decrease it.
      </p>

      <div className="shap-features">
        {top_features.map((feature, index) => {
          const isPositive = (feature.impact || 0) >= 0;
          const percentage =
            maxAbsValue > 0 ? Math.abs(feature.impact || 0) / maxAbsValue : 0;

          return (
            <div key={index} className="shap-feature">
              <div className="feature-name">
                <span className="name-text">
                  {feature.name || feature.feature || `Feature ${index + 1}`}
                </span>
                <span className={`feature-value ${isPositive ? "positive" : "negative"}`}>
                  {isPositive ? "+" : "-"}
                  {Math.abs(feature.impact || 0).toFixed(2)}
                </span>
              </div>

              <div className="feature-bar-container">
                <div
                  className={`feature-bar ${isPositive ? "positive" : "negative"}`}
                  style={{ width: `${percentage * 100}%` }}
                  role="progressbar"
                  aria-valuenow={percentage * 100}
                  aria-valuemin="0"
                  aria-valuemax="100"
                ></div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="shap-legend">
        <div className="legend-item">
          <div className="legend-color positive"></div>
          <span>Increases price</span>
        </div>
        <div className="legend-item">
          <div className="legend-color negative"></div>
          <span>Decreases price</span>
        </div>
      </div>
    </div>
  );
}
