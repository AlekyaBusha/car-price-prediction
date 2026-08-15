function TimingRecommendation({ forecast }) {
  if (!forecast || forecast.length < 2) {
    return null;
  }

  const current = Number(forecast[0]?.price) || 0;

  const sixMonths =
    Number(
      forecast.find((item) => item.months === 6)?.price
    ) || current;

  const twelveMonths =
    Number(
      forecast.find((item) => item.months === 12)?.price
    ) || current;

  const twentyFourMonths =
    Number(
      forecast.find((item) => item.months === 24)?.price
    ) || current;

  const change24 =
    current > 0
      ? ((twentyFourMonths - current) / current) * 100
      : 0;

  let title;
  let message;
  let icon;

  if (change24 <= -10) {
    icon = "📉";
    title = "Good Time to Sell";
    message =
      "The forecast indicates a significant decrease in the estimated vehicle price over the next 24 months.";
  } else if (change24 <= -3) {
    icon = "⚠️";
    title = "Consider Selling Soon";
    message =
      "The forecast suggests that the vehicle price may gradually decrease over the next 24 months.";
  } else if (change24 < 3) {
    icon = "➡️";
    title = "Price Looks Relatively Stable";
    message =
      "The forecast suggests relatively stable pricing over the next 24 months.";
  } else {
    icon = "⏳";
    title = "Consider Waiting";
    message =
      "The forecast does not indicate a significant price decrease over the next 24 months.";
  }

  return (
    <section
      style={{
        marginTop: "40px",
        padding: "24px",
        background: "#ffffff",
        border: "1px solid #e5e7eb",
        borderRadius: "12px",
      }}
    >
      <h2 className="section-header">
        Timing Recommendation
      </h2>

      <div
        style={{
          marginTop: "20px",
          padding: "20px",
          borderRadius: "10px",
          background: "#f8fafc",
        }}
      >
        <h3
          style={{
            margin: 0,
            fontSize: "20px",
          }}
        >
          {icon} {title}
        </h3>

        <p
          style={{
            marginTop: "10px",
            color: "#555",
            lineHeight: "1.6",
          }}
        >
          {message}
        </p>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(130px, 1fr))",
            gap: "12px",
            marginTop: "20px",
          }}
        >
          <div>
            <strong>Current</strong>
            <div>
              ₹
              {current.toLocaleString("en-IN", {
                maximumFractionDigits: 0,
              })}
            </div>
          </div>

          <div>
            <strong>+6 Months</strong>
            <div>
              ₹
              {sixMonths.toLocaleString("en-IN", {
                maximumFractionDigits: 0,
              })}
            </div>
          </div>

          <div>
            <strong>+12 Months</strong>
            <div>
              ₹
              {twelveMonths.toLocaleString("en-IN", {
                maximumFractionDigits: 0,
              })}
            </div>
          </div>

          <div>
            <strong>+24 Months</strong>
            <div>
              ₹
              {twentyFourMonths.toLocaleString("en-IN", {
                maximumFractionDigits: 0,
              })}
            </div>
          </div>
        </div>

        <p
          style={{
            marginTop: "20px",
            fontWeight: "600",
          }}
        >
          24-month change:{" "}
          {change24 >= 0 ? "+" : ""}
          {change24.toFixed(1)}%
        </p>
      </div>
    </section>
  );
}

export default TimingRecommendation;