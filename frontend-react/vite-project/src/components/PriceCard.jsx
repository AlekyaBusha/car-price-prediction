import React from "react";

function formatPrice(value) {
  if (value === null || value === undefined || isNaN(value)) {
    return "₹ 0";
  }

  return `₹ ${Number(value).toLocaleString("en-IN", {
    maximumFractionDigits: 0,
  })}`;
}

function formatLakh(value) {
  if (value === null || value === undefined || isNaN(value)) {
    return "₹ 0";
  }

  return `₹ ${(Number(value) / 100000).toFixed(2)} Lakh`;
}

function PriceCard({ prediction, loading }) {
  const predictedPrice =
    prediction?.predicted_price ??
    prediction?.price ??
    prediction?.prediction ??
    0;

  const minimum =
    prediction?.minimum_price ??
    prediction?.min_price ??
    prediction?.price_range?.minimum ??
    prediction?.price_range?.min ??
    predictedPrice * 0.9;

  const maximum =
    prediction?.maximum_price ??
    prediction?.max_price ??
    prediction?.price_range?.maximum ??
    prediction?.price_range?.max ??
    predictedPrice * 1.1;

  const confidence =
    prediction?.confidence_score ??
    prediction?.confidence ??
    96;

  const recommendation =
    prediction?.recommendation ??
    "Good Deal";

  const recommendationText =
    prediction?.recommendation_text ??
    "You are getting a good deal for this car!";

  return (
    <section className="price-card">

      {/* Header */}
      <div className="section-heading">
        <div className="section-icon green-icon">₹</div>

        <div>
          <h2>Estimated Market Price</h2>
          <p>Based on your car details</p>
        </div>
      </div>

      {/* Main Price */}
      <div className="main-price">
        {loading ? (
          <span className="price-loading">
            Calculating...
          </span>
        ) : (
          formatPrice(predictedPrice)
        )}
      </div>

      {/* Confidence */}
      <div className="price-section">
        <div className="price-section-title">
          <span>Confidence Score</span>

          <strong>
            {Math.round(confidence)}%
          </strong>
        </div>

        <div className="confidence-bar">
          <div
            className="confidence-fill"
            style={{
              width: `${Math.min(
                100,
                Math.max(0, confidence)
              )}%`,
            }}
          />
        </div>
      </div>

      {/* Price Range */}
      <div className="price-section">
        <div className="price-section-title">
          <span>Price Range</span>

          <span className="info-icon">
            i
          </span>
        </div>

        <div className="price-range">
          <div>
            <strong>
              {formatLakh(minimum)}
            </strong>

            <small>Minimum</small>
          </div>

          <span className="range-dash">
            –
          </span>

          <div>
            <strong>
              {formatLakh(maximum)}
            </strong>

            <small>Maximum</small>
          </div>
        </div>
      </div>

      {/* Recommendation */}
      <div className="price-section recommendation-section">
        <h3>Recommendation</h3>

        <div className="recommendation-box">
          <span className="recommendation-dot" />

          <div>
            <strong>
              {recommendation}
            </strong>

            <p>
              {recommendationText}
            </p>
          </div>
        </div>
      </div>

    </section>
  );
}

export default PriceCard;