function PriceCard({ priceData }) {
  if (!priceData) return null

  return (
    <section>
      <h2 className="section-header">Predicted Price</h2>
      <div className="grid-3">
        <div className="price-card">
          <div className="price-label">Low Estimate</div>
          <div className="price-value">
            ₹{priceData.low.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </div>
        </div>
        <div className="price-card">
          <div className="price-label">Fair Price</div>
          <div className="price-value">
            ₹{priceData.predicted.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </div>
        </div>
        <div className="price-card">
          <div className="price-label">High Estimate</div>
          <div className="price-value">
            ₹{priceData.high.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </div>
        </div>
      </div>
    </section>
  )
}

export default PriceCard