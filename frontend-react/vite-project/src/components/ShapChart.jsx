import React from "react";

function ShapChart({ contributions = [] }) {
  const factors = contributions
    .filter(
      (item) =>
        item &&
        item.feature &&
        item.impact !== undefined &&
        item.impact !== null
    )
    .map((item) => ({
      feature: item.feature,
      impact: Number(item.impact),
    }))
    .sort((a, b) => Math.abs(b.impact) - Math.abs(a.impact))
    .slice(0, 6);

  const maxImpact = Math.max(
    ...factors.map((item) => Math.abs(item.impact)),
    1
  );

  return (
    <section className="shap-card">
      <div className="section-heading">
        <div className="section-icon purple-icon">✦</div>

        <div>
          <h2>Why This Price?</h2>
          <p>
            Top factors influencing the predicted price (SHAP Analysis)
          </p>
        </div>
      </div>

      {factors.length === 0 ? (
        <div className="shap-empty">
          <p>
            Enter the vehicle details and click
            <strong> Predict Price </strong>
            to see the factors influencing the prediction.
          </p>
        </div>
      ) : (
        <div className="shap-list">
          {factors.map((item, index) => {
            const absoluteImpact = Math.abs(item.impact);

            const percentage = Math.min(
              100,
              (absoluteImpact / maxImpact) * 100
            );

            return (
              <div
                className="shap-row"
                key={`${item.feature}-${index}`}
              >
                <div className="shap-label">
                  <span>{item.feature}</span>

                  <strong
                    className={
                      item.impact >= 0
                        ? "positive-impact"
                        : "negative-impact"
                    }
                  >
                    {item.impact >= 0 ? "+" : ""}
                    {item.impact.toFixed(2)}
                  </strong>
                </div>

                <div className="shap-bar">
                  <div
                    className="shap-fill"
                    style={{
                      width: `${percentage}%`,
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      )}

      <div className="shap-info">
        <span>ⓘ</span>

        <p>
          Positive values push the prediction higher;
          negative values push it lower.
        </p>
      </div>
    </section>
  );
}

export default ShapChart;