/**
 * ForecastChart.jsx
 * Display price forecast as a bar or line chart
 */

import "../styles/ForecastChart.css";

export default function ForecastChart({ forecast = [], loading }) {
  if (loading) {
    return (
      <div className="forecast-container">
        <p className="loading-text">Loading forecast...</p>
      </div>
    );
  }

  if (!forecast || forecast.length === 0) {
    return (
      <div className="forecast-container">
        <p className="no-data-message">No forecast data available.</p>
      </div>
    );
  }

  // Find min and max prices for scaling
  const prices = forecast
    .map((item) => item.price || item.predicted_price || 0)
    .filter((p) => p > 0);

  if (prices.length === 0) {
    return (
      <div className="forecast-container">
        <p className="no-data-message">No valid forecast data available.</p>
      </div>
    );
  }

  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const priceRange = maxPrice - minPrice || 1;

  // Calculate heights relative to max price
  const calculateHeight = (price) => {
    return ((price - minPrice) / priceRange) * 100 || 0;
  };

  const formatPrice = (price) => {
    if (!price && price !== 0) return "N/A";
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(price);
  };

  const formatMonth = (monthsFromNow) => {
    if (!monthsFromNow) return "Current";
    if (monthsFromNow === 1) return "1 Month";
    if (monthsFromNow === 3) return "3 Months";
    if (monthsFromNow === 6) return "6 Months";
    if (monthsFromNow === 12) return "1 Year";
    if (monthsFromNow === 24) return "2 Years";
    return `${monthsFromNow} Months`;
  };

  return (
    <div className="forecast-container">
      <h3 className="section-title">Price Forecast</h3>

      <p className="forecast-description">
        Predicted price changes over time based on vehicle depreciation and market trends.
      </p>

      {/* Chart */}
      <div className="forecast-chart">
        <div className="chart-bars">
          {forecast.map((item, index) => {
            const price = item.price || item.predicted_price || 0;
            const height = calculateHeight(price);

            const isCurrent = (item.months || 0) === 0 || index === 0;

            return (
              <div key={index} className="bar-column">
                <div className="bar-container">
                  <div
                    className={`bar ${isCurrent ? "current-bar" : ""}`}
                    style={{ height: `${height}%` }}
                    title={`${formatMonth(item.months || 0)}: ${formatPrice(price)}`}
                  >
                    <span className="bar-price">
                      {formatPrice(price)}
                    </span>
                  </div>
                </div>
                <span className={`bar-label ${isCurrent ? "current-label" : ""}`}>
                  {formatMonth(item.months || 0)}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Forecast Table */}
      <div className="forecast-table">
        <table>
          <thead>
            <tr>
              <th>Time Period</th>
              <th>Predicted Price</th>
              <th>Change</th>
            </tr>
          </thead>
          <tbody>
            {forecast.map((item, index) => {
              const price = item.price || item.predicted_price || 0;
              const previousPrice =
                index > 0
                  ? forecast[index - 1].price ||
                    forecast[index - 1].predicted_price ||
                    0
                  : price;
              const change = price - previousPrice;
              const changePercent =
                previousPrice > 0 ? (change / previousPrice) * 100 : 0;

              return (
                <tr key={index}>
                  <td className="time-cell">
                    {formatMonth(item.months || 0)}
                  </td>
                  <td className="price-cell">{formatPrice(price)}</td>
                  <td className={`change-cell ${change >= 0 ? "positive" : "negative"}`}>
                    {change >= 0 ? "+" : ""}
                    {formatPrice(change)}
                    <span className="percent">
                      ({changePercent >= 0 ? "+" : ""}
                      {changePercent.toFixed(1)}%)
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
