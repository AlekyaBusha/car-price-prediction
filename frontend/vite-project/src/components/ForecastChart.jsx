function ForecastChart({ forecast }) {

  if (!forecast || forecast.length === 0) {
    return null;
  }


  const maxForecastPrice = Math.max(
    ...forecast.map(
      (f) => Number(f.price) || 0
    )
  );


  return (
    <div
      className="forecast-chart"
      style={{
        display: "flex",
        alignItems: "flex-end",
        justifyContent: "space-around",
        gap: "20px",
        minHeight: "220px",
        width: "100%",
        padding: "20px 10px",
        boxSizing: "border-box",
      }}
    >

      {forecast.map((point) => {

        const price =
          Number(point.price) || 0;


        const barHeight =
          maxForecastPrice > 0
            ? (price / maxForecastPrice) * 150
            : 0;


        return (
          <div
            key={point.months}
            className="forecast-bar-wrapper"
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "flex-end",
              minWidth: "70px",
            }}
          >

            {/* Price */}

            <span
              className="forecast-price"
              style={{
                marginBottom: "8px",
                fontWeight: "600",
                fontSize: "14px",
              }}
            >
              ₹
              {price.toLocaleString(
                "en-IN",
                {
                  maximumFractionDigits: 0,
                }
              )}
            </span>


            {/* Bar */}

            <div
              className="forecast-bar"
              style={{
                width: "45px",
                height: `${barHeight}px`,
                background: "#2563eb",
                borderRadius:
                  "6px 6px 0 0",
                minHeight:
                  price > 0 ? "5px" : "0",
              }}
            />


            {/* Time */}

            <span
              className="forecast-label"
              style={{
                marginTop: "10px",
                fontSize: "14px",
                fontWeight: "500",
              }}
            >
              {point.months === 0
                ? "Now"
                : `+${point.months}mo`}
            </span>

          </div>
        );

      })}

    </div>
  );
}


export default ForecastChart;