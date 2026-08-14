function ForecastChart({ forecast }) {
  if (!forecast || forecast.length === 0) return null

  const maxForecastPrice = Math.max(...forecast.map(f => f.price))

  return (
    <div className="forecast-chart">
      {forecast.map(point => (
        <div key={point.months} className="forecast-bar-wrapper">
          <div
            className="forecast-bar"
            style={{ height: `${(point.price / maxForecastPrice) * 150}px` }}
          />
          <span className="forecast-label">+{point.months}mo</span>
          <span className="forecast-price">₹{Math.round(point.price / 1000)}K</span>
        </div>
      ))}
    </div>
  )
}

export default ForecastChart