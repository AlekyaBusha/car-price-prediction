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

  const isPositive = change24 >= 0;
  const changeColor = change24 <= -10 ? "#EF4444" : change24 <= -3 ? "#F59E0B" : change24 < 3 ? "#42A5F5" : "#35E875";

  return (
    <section
      style={{
        marginTop: "24px",
        padding: "24px",
        background: "#0D1B2A",
        border: "1px solid #26384A",
        borderRadius: "16px",
        boxShadow: "0 8px 24px rgba(0,0,0,0.25)",
        color: "#F1F5F9",
      }}
    >
      <h3
        style={{
          margin: "0 0 4px 0",
          fontSize: "18px",
          fontWeight: 700,
          color: "#F1F5F9",
        }}
      >
        ⏱️ Timing Recommendation
      </h3>
      <p style={{ margin: "0 0 16px 0", fontSize: "13px", color: "#A8B3C2" }}>
        AI market depreciation analysis for optimal buying or selling decisions.
      </p>

      <div
        style={{
          padding: "20px",
          borderRadius: "12px",
          background: "#0B1725",
          border: "1px solid #26384A",
        }}
      >
        <h4
          style={{
            margin: 0,
            fontSize: "18px",
            fontWeight: 700,
            color: "#F1F5F9",
            display: "flex",
            alignItems: "center",
            gap: "8px",
          }}
        >
          <span>{icon}</span> <span>{title}</span>
        </h4>

        <p
          style={{
            marginTop: "10px",
            color: "#A8B3C2",
            lineHeight: "1.6",
            fontSize: "14px",
          }}
        >
          {message}
        </p>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))",
            gap: "12px",
            marginTop: "20px",
          }}
        >
          <div
            style={{
              background: "rgba(14, 23, 38, 0.7)",
              padding: "12px 14px",
              borderRadius: "8px",
              border: "1px solid #26384A",
            }}
          >
            <span style={{ fontSize: "12px", color: "#A8B3C2", fontWeight: 600, display: "block", marginBottom: "4px" }}>
              Current
            </span>
            <div style={{ fontSize: "16px", fontWeight: 700, color: "#35E875" }}>
              ₹{current.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
            </div>
          </div>

          <div
            style={{
              background: "rgba(14, 23, 38, 0.7)",
              padding: "12px 14px",
              borderRadius: "8px",
              border: "1px solid #26384A",
            }}
          >
            <span style={{ fontSize: "12px", color: "#A8B3C2", fontWeight: 600, display: "block", marginBottom: "4px" }}>
              +6 Months
            </span>
            <div style={{ fontSize: "16px", fontWeight: 700, color: "#42A5F5" }}>
              ₹{sixMonths.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
            </div>
          </div>

          <div
            style={{
              background: "rgba(14, 23, 38, 0.7)",
              padding: "12px 14px",
              borderRadius: "8px",
              border: "1px solid #26384A",
            }}
          >
            <span style={{ fontSize: "12px", color: "#A8B3C2", fontWeight: 600, display: "block", marginBottom: "4px" }}>
              +12 Months
            </span>
            <div style={{ fontSize: "16px", fontWeight: 700, color: "#42A5F5" }}>
              ₹{twelveMonths.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
            </div>
          </div>

          <div
            style={{
              background: "rgba(14, 23, 38, 0.7)",
              padding: "12px 14px",
              borderRadius: "8px",
              border: "1px solid #26384A",
            }}
          >
            <span style={{ fontSize: "12px", color: "#A8B3C2", fontWeight: 600, display: "block", marginBottom: "4px" }}>
              +24 Months
            </span>
            <div style={{ fontSize: "16px", fontWeight: 700, color: "#42A5F5" }}>
              ₹{twentyFourMonths.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
            </div>
          </div>
        </div>

        <div
          style={{
            marginTop: "18px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            paddingTop: "14px",
            borderTop: "1px solid #26384A",
            fontSize: "13px",
            fontWeight: 600,
          }}
        >
          <span style={{ color: "#A8B3C2" }}>Expected 24-Month Change:</span>
          <span style={{ color: changeColor, fontSize: "14px" }}>
            {isPositive ? "+" : ""}
            {change24.toFixed(1)}%
          </span>
        </div>
      </div>
    </section>
  );
}

export default TimingRecommendation;