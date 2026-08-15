function PriceCard({ priceData }) {
  if (!priceData) {
    return null;
  }

  // Backend returns:
  //
  // price_range: {
  //   low,
  //   predicted,
  //   high
  // }

  const priceRange = priceData.price_range;

  if (!priceRange) {
    return null;
  }

  return (
    <section>
      <h2 className="section-header">
        Predicted Price
      </h2>

      <div className="grid-3">

        {/* LOW ESTIMATE */}

        <div className="price-card">
          <div className="price-label">
            Low Estimate
          </div>

          <div className="price-value">
            ₹
            {Number(priceRange.low).toLocaleString(
              "en-IN",
              {
                maximumFractionDigits: 0,
              }
            )}
          </div>
        </div>

        {/* FAIR PRICE */}

        <div className="price-card">
          <div className="price-label">
            Fair Price
          </div>

          <div className="price-value">
            ₹
            {Number(priceRange.predicted).toLocaleString(
              "en-IN",
              {
                maximumFractionDigits: 0,
              }
            )}
          </div>
        </div>

        {/* HIGH ESTIMATE */}

        <div className="price-card">
          <div className="price-label">
            High Estimate
          </div>

          <div className="price-value">
            ₹
            {Number(priceRange.high).toLocaleString(
              "en-IN",
              {
                maximumFractionDigits: 0,
              }
            )}
          </div>
        </div>

      </div>
    </section>
  );
}

export default PriceCard;