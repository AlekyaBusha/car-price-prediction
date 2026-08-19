import "./Header.css";

function Header({ activeNav = "predict", onSelectNav }) {
  const navItems = [
    { id: "predict", label: "Predict Price", icon: "🚗" },
  ];

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-brand">
          <h1>🚗 Used Car Price Prediction</h1>
          <p>
            AI-powered used car valuation using Machine Learning
          </p>
        </div>

        <nav className="header-nav" aria-label="Main Navigation">
          {navItems.map((item) => (
            <button
              key={item.id}
              type="button"
              className={`header-nav-btn ${activeNav === item.id ? "active" : ""}`}
              onClick={() => onSelectNav && onSelectNav(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
}

export default Header;