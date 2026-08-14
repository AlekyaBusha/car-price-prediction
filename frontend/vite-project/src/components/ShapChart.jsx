function ShapChart({ contributions }) {
  if (!contributions || contributions.length === 0) return null

  const maxAbsImpact = Math.max(...contributions.map(c => Math.abs(c.impact)))

  return (
    <section>
      <h2 className="section-header">Why This Price</h2>
      <div className="shap-chart">
        {contributions.map(item => (
          <div key={item.feature} className="shap-row">
            <span className="shap-label">{item.feature}</span>
            <div className="shap-bar-track">
              <div
                className={item.impact >= 0 ? "shap-bar-positive" : "shap-bar-negative"}
                style={{ width: `${(Math.abs(item.impact) / maxAbsImpact) * 100}%` }}
              />
            </div>
            <span className={item.impact >= 0 ? "feature-positive" : "feature-negative"}>
              {item.impact >= 0 ? "▲" : "▼"} ₹{Math.abs(item.impact).toLocaleString(undefined, { maximumFractionDigits: 0 })}
            </span>
          </div>
        ))}
      </div>
    </section>
  )
}

export default ShapChart