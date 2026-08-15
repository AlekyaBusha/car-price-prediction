import React from "react";
import "./Header.css";

function Header() {
  return (
    <header className="app-header">
      <div className="header-left">
        <div className="header-car-icon">🚗</div>

        <div>
          <h1>AI Car Price Prediction</h1>
          <p>AI-powered used car valuation using Machine Learning</p>
        </div>
      </div>

      <div className="header-trust">
        <div className="trust-icon">✓</div>

        <div>
          <strong>Trusted Predictions</strong>
          <span>Accurate • Reliable • Smart</span>
        </div>
      </div>
    </header>
  );
}

export default Header;