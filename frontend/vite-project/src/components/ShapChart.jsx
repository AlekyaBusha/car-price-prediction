function ShapChart({ contributions }) {
  if (!contributions || contributions.length === 0) {
    return null;
  }

  const maxAbsImpact = Math.max(
    ...contributions.map((item) =>
      Math.abs(Number(item.impact) || 0)
    ),
    1
  );

  function formatFeatureName(feature) {
    return String(feature)
      .replace(/^brand_/, "Brand: ")
      .replace(/^seller_type_/, "Seller: ")
      .replace(/^fuel_type_/, "Fuel: ")
      .replace(/^transmission_type_/, "Transmission: ")
      .replace(/_/g, " ")
      .replace(/\b\w/g, (char) =>
        char.toUpperCase()
      );
  }

  return (
    <section style={{ marginTop: "30px" }}>
      <h2 className="section-header">
        Why This Price
      </h2>

      <p
        style={{
          color: "#6B7280",
          marginBottom: "20px",
        }}
      >
        These are the most important factors that
        influenced the predicted price.
      </p>

      <div className="shap-chart">
        {contributions.map((item, index) => {
          const impact = Number(item.impact) || 0;

          const width =
            (Math.abs(impact) / maxAbsImpact) * 100;

          const isPositive = impact >= 0;

          return (
            <div
              key={`${item.feature}-${index}`}
              className="shap-row"
            >
              {/* Feature name */}

              <span className="shap-label">
                {formatFeatureName(item.feature)}
              </span>

              {/* Bar */}

              <div className="shap-bar-track">
                <div
                  className={
                    isPositive
                      ? "shap-bar-positive"
                      : "shap-bar-negative"
                  }
                  style={{
                    width: `${width}%`,
                  }}
                />
              </div>

              {/* Impact */}

              <span
                className={
                  isPositive
                    ? "feature-positive"
                    : "feature-negative"
                }
              >
                {isPositive ? "▲" : "▼"} ₹
                {Math.abs(impact).toLocaleString(
                  "en-IN",
                  {
                    maximumFractionDigits: 0,
                  }
                )}
              </span>
            </div>
          );
        })}
      </div>

      {/* Legend */}

      <div
        style={{
          display: "flex",
          gap: "20px",
          marginTop: "16px",
          fontSize: "14px",
          color: "#6B7280",
        }}
      >
        <span>
          ▲ Increases predicted price
        </span>

        <span>
          ▼ Decreases predicted price
        </span>
      </div>
    </section>
  );
}

export default ShapChart;