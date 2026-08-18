/**
 * AccuracyPage.jsx
 * Dedicated Accuracy page displaying the "Comparison of Model Evaluation Metrics"
 * 4-bar metric graph (Accuracy, Precision, Recall, F1 Score).
 */

import { useState, useEffect } from "react";
import { fetchAccuracyMetrics } from "../services/api";
import "../styles/AccuracyPage.css";

export default function AccuracyPage({ onNavigateToPredict }) {
  const [metricsData, setMetricsData] = useState([
    { name: "Accuracy", value: 0.97, formatted: "0.97" },
    { name: "Precision", value: 1.00, formatted: "1.00" },
    { name: "Recall", value: 0.10, formatted: "0.10" },
    { name: "F1 Score", value: 0.18, formatted: "0.18" },
  ]);

  useEffect(() => {
    async function loadMetrics() {
      try {
        const res = await fetchAccuracyMetrics();
        if (res && res.metrics && Array.isArray(res.metrics)) {
          setMetricsData(res.metrics);
        }
      } catch (e) {
        console.warn("Using default accuracy metrics:", e);
      }
    }
    loadMetrics();
  }, []);

  const yTicks = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0];

  return (
    <div className="accuracy-page-container">
      {/* Top Header Bar */}
      <div className="accuracy-header">
        <div>
          <h2 className="accuracy-title">📊 Model Accuracy & Evaluation</h2>
          <p className="accuracy-subtitle">
            Performance comparison of standard model evaluation metrics.
          </p>
        </div>
        {onNavigateToPredict && (
          <button
            type="button"
            className="btn-back-predictor"
            onClick={onNavigateToPredict}
          >
            🚗 Back to Predictor
          </button>
        )}
      </div>

      {/* Main Chart Card */}
      <div className="accuracy-chart-card">
        <h3 className="chart-main-title">Comparison of Model Evaluation Metrics</h3>

        <div className="chart-wrapper">
          {/* Y-Axis scale */}
          <div className="y-axis">
            {yTicks.map((tick) => (
              <span key={tick} className="y-tick">
                {tick.toFixed(1)}
              </span>
            ))}
          </div>

          {/* Chart Plot Area */}
          <div className="chart-plot-area">
            {/* Horizontal Gridlines */}
            <div className="gridlines-container">
              {yTicks.map((tick) => (
                <div key={tick} className="gridline" />
              ))}
            </div>

            {/* Bars Container */}
            <div className="bars-container">
              {metricsData.map((item, idx) => {
                const heightPercent = Math.max(2, Math.min(100, item.value * 100));

                return (
                  <div key={idx} className="bar-column">
                    {/* Value Badge Above Bar */}
                    <div className="bar-value-label">
                      {typeof item.value === "number" ? item.value.toFixed(2) : item.formatted}
                    </div>

                    {/* Bar Track & Fill */}
                    <div className="bar-track">
                      <div
                        className="bar-fill"
                        style={{
                          height: `${heightPercent}%`,
                        }}
                        title={`${item.name}: ${item.value}`}
                      />
                    </div>

                    {/* X-Axis Category Label */}
                    <div className="bar-category-label">{item.name}</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
