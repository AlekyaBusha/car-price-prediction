/**
 * ErrorMessage.jsx
 * Reusable error message component
 */

import "../styles/ErrorMessage.css";

export default function ErrorMessage({ message, onDismiss }) {
  return (
    <div className="error-banner">
      <div className="error-content">
        <span className="error-icon">⚠</span>
        <p className="error-text">{message}</p>
        {onDismiss && (
          <button
            className="error-close"
            onClick={onDismiss}
            aria-label="Dismiss error"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
}
