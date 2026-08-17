/**
 * AboutSection.jsx
 * Information about the application
 */

import "../styles/AboutSection.css";

export default function AboutSection() {
  return (
    <section className="about-section">
      <div className="about-container">
        <h2 className="about-title">About Car Price Prediction</h2>

        <div className="about-content">
          <div className="about-card">
            <div className="about-icon">📊</div>
            <h3>AI-Powered Predictions</h3>
            <p>
              Our advanced XGBoost machine learning models analyze market trends and
              vehicle specifications to provide accurate price predictions.
            </p>
          </div>

          <div className="about-card">
            <div className="about-icon">🔍</div>
            <h3>Explainable AI</h3>
            <p>
              Understand which features influence the price with SHAP (SHapley Additive
              exPlanations) feature importance analysis.
            </p>
          </div>

          <div className="about-card">
            <div className="about-icon">📈</div>
            <h3>Price Forecasting</h3>
            <p>
              Get insights into how your car's price will depreciate over time with our
              price forecast engine.
            </p>
          </div>

          <div className="about-card">
            <div className="about-icon">🚗</div>
            <h3>Variant Comparison</h3>
            <p>
              Compare different configurations of the same car model to find the best
              value for your needs.
            </p>
          </div>
        </div>

        <div className="about-features">
          <h3>Key Features</h3>
          <ul>
            <li>Real-time price predictions based on market data</li>
            <li>Comprehensive vehicle variant comparison</li>
            <li>Feature importance visualization</li>
            <li>6-month to 2-year price forecasts</li>
            <li>Support for multiple car brands and models</li>
            <li>Responsive design for all devices</li>
          </ul>
        </div>

        <div className="about-footer">
          <p>
            This application uses machine learning to help you make informed decisions
            about used car purchases and sales.
          </p>
        </div>
      </div>
    </section>
  );
}
