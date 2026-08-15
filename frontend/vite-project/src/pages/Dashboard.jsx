import { useState } from "react";

import Header from "../components/Header/Header";
import CarForm from "../components/CarForm.jsx";
import PriceCard from "../components/PriceCard.jsx";
import ShapChart from "../components/ShapChart.jsx";
import ForecastChart from "../components/ForecastChart.jsx";
import TimingRecommendation from "../components/TimingRecommendation.jsx";


function Dashboard() {

  const [prediction, setPrediction] = useState(null);


  function handlePrediction(result) {

    console.log("Dashboard received prediction:");
    console.log(result);

    setPrediction(result);

  }


  return (
    <>
      <Header />

      <main className="container">

        {/* ==============================
            CAR FORM
        ============================== */}

        <CarForm
          onPrediction={handlePrediction}
        />


        {/* ==============================
            RESULTS
        ============================== */}

        {prediction && (

          <div
            style={{
              marginTop: "40px",
              paddingBottom: "50px",
            }}
          >

            {/* ==========================
                PRICE RANGE
            ========================== */}

            <PriceCard
              priceData={{
                low:
                  prediction.price_range?.low ??
                  prediction.predicted_price,

                predicted:
                  prediction.price_range?.predicted ??
                  prediction.predicted_price,

                high:
                  prediction.price_range?.high ??
                  prediction.predicted_price,
              }}
            />


            {/* ==========================
                SHAP
            ========================== */}

            {prediction.explanation &&
              prediction.explanation.top_features &&
              prediction.explanation.top_features.length > 0 && (

                <div
                  style={{
                    marginTop: "40px",
                  }}
                >

                  <ShapChart
                    contributions={
                      prediction.explanation.top_features
                    }
                  />

                </div>

              )}


            {/* ==========================
                FORECAST
            ========================== */}

            {prediction.forecast &&
              prediction.forecast.length > 0 && (

                <div
                  style={{
                    marginTop: "40px",
                    padding: "24px",
                    background: "#ffffff",
                    borderRadius: "12px",
                    border: "1px solid #e5e7eb",
                  }}
                >

                  <h2 className="section-header">
                    Price Forecast
                  </h2>


                  <p
                    style={{
                      color: "#666",
                      marginBottom: "25px",
                    }}
                  >
                    Estimated vehicle price over
                    the next 24 months.
                  </p>


                  <ForecastChart
                    forecast={prediction.forecast}
                  />
                  <TimingRecommendation
  forecast={prediction.forecast}
/>

                </div>

              )}

          </div>

        )}

      </main>
    </>
  );
}


export default Dashboard;