import React from "react";

function ForecastChart({ forecast = [] }) {
  const data = forecast
    .filter(
      (item) =>
        item &&
        item.months !== undefined &&
        item.price !== undefined
    )
    .map((item) => ({
      months: Number(item.months),
      price: Number(item.price),
    }));

  const prices = data.map((item) => item.price);

  const maxPrice = Math.max(...prices, 1);
  const minPrice = Math.min(...prices, 0);

  const getYearLabel = (months) => {
    if (months === 0) {
      return "Today";
    }

    if (months % 12 === 0) {
      return `+${months / 12} Year`;
    }

    return `+${months} Months`;
  };

  const formatLakh = (price) =>
    `₹ ${(price / 100000).toFixed(2)} Lakh`;

  return (
    <section className="forecast-card">

      <div className="section-heading">
        <div className="section-icon forecast-icon">
          ↗
        </div>

        <div>
          <h2>Future Price Forecast</h2>

          <p>
            Predicted price trend for the next 2 years
          </p>
        </div>
      </div>

      {data.length === 0 ? (
        <div className="forecast-empty">
          <p>
            Enter the vehicle details and click
            <strong> Predict Price </strong>
            to see the future price forecast.
          </p>
        </div>
      ) : (
        <>
          <div className="chart-wrapper">

            <div className="y-axis">
              <span>
                ₹ {(maxPrice / 100000).toFixed(1)}L
              </span>

              <span>
                ₹ {((maxPrice * 0.75) / 100000).toFixed(1)}L
              </span>

              <span>
                ₹ {((maxPrice * 0.5) / 100000).toFixed(1)}L
              </span>

              <span>
                ₹ {((maxPrice * 0.25) / 100000).toFixed(1)}L
              </span>
            </div>

            <div className="forecast-chart">

              <div className="grid-line line-1" />
              <div className="grid-line line-2" />
              <div className="grid-line line-3" />
              <div className="grid-line line-4" />

              <div className="forecast-points">

                {data.map((item, index) => {

                  const price = item.price;

                  const range =
                    maxPrice - minPrice || 1;

                  const bottom =
                    15 +
                    ((price - minPrice) / range) *
                      65;

                  const left =
                    data.length === 1
                      ? 50
                      : 10 +
                        (index /
                          (data.length - 1)) *
                          80;

                  return (
                    <div
                      className="forecast-point"
                      key={`${item.months}-${index}`}
                      style={{
                        left: `${left}%`,
                        bottom: `${bottom}%`,
                      }}
                    >

                      <div className="forecast-tooltip">
                        {formatLakh(price)}
                      </div>

                      <div className="forecast-dot" />

                      <span className="forecast-year">
                        {getYearLabel(item.months)}
                      </span>

                    </div>
                  );
                })}

              </div>
            </div>
          </div>

          <div className="forecast-legend">
            <span className="legend-line" />

            <span>
              Predicted Price
            </span>
          </div>
        </>
      )}

    </section>
  );
}

export default ForecastChart;