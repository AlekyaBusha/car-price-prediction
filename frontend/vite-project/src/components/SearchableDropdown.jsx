import { useEffect, useRef, useState } from "react";

function SearchableDropdown({
  label,
  options = [],
  value,
  onChange,
  placeholder = "Search...",
  disabled = false,
  required = false,
}) {
  const [search, setSearch] = useState(
    value !== null && value !== undefined ? String(value) : ""
  );

  const [isOpen, setIsOpen] = useState(false);

  const containerRef = useRef(null);

  // ---------------------------------------------------------
  // Sync selected value when dropdown is closed
  // ---------------------------------------------------------

  useEffect(() => {
    if (!isOpen) {
      setSearch(value !== null && value !== undefined ? String(value) : "");
    }
  }, [value, isOpen]);

  // ---------------------------------------------------------
  // Close when clicking outside
  // ---------------------------------------------------------

  useEffect(() => {
    function handleClickOutside(event) {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target)
      ) {
        setIsOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  // ---------------------------------------------------------
  // Search
  // ---------------------------------------------------------

  const searchText = String(search ?? "").toLowerCase();

  const filteredOptions = options.filter((option) => {
    const optionText = String(option ?? "").toLowerCase();
    return optionText.includes(searchText);
  });

  // ---------------------------------------------------------
  // Open dropdown
  // ---------------------------------------------------------

  function handleFocus() {
    if (disabled) {
      return;
    }

    setIsOpen(true);
  }

  // ---------------------------------------------------------
  // Handle typing - commits value immediately to form
  // ---------------------------------------------------------

  function handleSearch(event) {
    const inputValue = event.target.value;

    setSearch(inputValue);
    setIsOpen(true);
    onChange(inputValue);
  }

  // ---------------------------------------------------------
  // Handle Blur - ensure typed value is committed
  // ---------------------------------------------------------

  function handleBlur() {
    if (search !== value) {
      onChange(search);
    }
  }

  // ---------------------------------------------------------
  // Select option
  // ---------------------------------------------------------

  function handleSelect(option) {
    const strVal = String(option);
    setSearch(strVal);
    onChange(option);
    setIsOpen(false);
  }

  // ---------------------------------------------------------
  // Keyboard
  // ---------------------------------------------------------

  function handleKeyDown(event) {
    if (event.key === "Enter") {
      event.preventDefault();

      if (filteredOptions.length === 1) {
        handleSelect(filteredOptions[0]);
      } else {
        setIsOpen(false);
        onChange(search);
      }
    }

    if (event.key === "Escape") {
      setIsOpen(false);
      setSearch(value !== null && value !== undefined ? String(value) : "");
    }
  }

  // ---------------------------------------------------------
  // UI
  // ---------------------------------------------------------

  return (
    <div
      ref={containerRef}
      style={{
        position: "relative",
        marginTop: "16px",
      }}
    >
      <label style={{ display: "block", marginBottom: "6px", fontSize: "13px", fontWeight: 600, color: "#E2E8F0" }}>
        {label}
        {required && (
          <span
            className="required-star"
            style={{
              color: "#EF4444",
              fontWeight: 700,
              marginLeft: "4px",
            }}
          >
            *
          </span>
        )}
      </label>

      <div
        style={{
          position: "relative",
        }}
      >
        <input
          type="text"
          value={search}
          placeholder={placeholder}
          disabled={disabled}
          onFocus={handleFocus}
          onBlur={handleBlur}
          onChange={handleSearch}
          onKeyDown={handleKeyDown}
          style={{
            width: "100%",
            padding: "11px 36px 11px 12px",
            boxSizing: "border-box",
            border: "1px solid var(--border)",
            borderRadius: "8px",
            fontSize: "14px",
            outline: "none",
            background: disabled ? "var(--muted-bg)" : "rgba(14, 23, 38, 0.7)",
            color: disabled ? "var(--muted-text)" : "var(--text)",
            cursor: disabled ? "not-allowed" : "text",
            transition: "border-color 0.2s ease, box-shadow 0.2s ease",
          }}
        />

        <span
          style={{
            position: "absolute",
            right: "12px",
            top: "50%",
            transform: "translateY(-50%)",
            pointerEvents: "none",
            color: "var(--muted-text)",
            fontSize: "11px",
          }}
        >
          {isOpen ? "▲" : "▼"}
        </span>
      </div>

      {isOpen && !disabled && (
        <div
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            right: 0,
            marginTop: "4px",
            background: "#111C2E",
            border: "1px solid var(--border)",
            borderRadius: "8px",
            maxHeight: "220px",
            overflowY: "auto",
            zIndex: 1000,
            boxShadow: "0 10px 25px rgba(0,0,0,0.5)",
          }}
        >
          {filteredOptions.length > 0 ? (
            filteredOptions.map((option, index) => (
              <div
                key={`${String(option)}-${index}`}
                onMouseDown={(event) => {
                  event.preventDefault();
                  handleSelect(option);
                }}
                style={{
                  padding: "10px 12px",
                  cursor: "pointer",
                  borderBottom: "1px solid rgba(148, 163, 184, 0.1)",
                  fontSize: "14px",
                  color: "var(--text)",
                  transition: "background 0.15s ease",
                }}
                onMouseEnter={(event) => {
                  event.currentTarget.style.background = "#1E2D4A";
                }}
                onMouseLeave={(event) => {
                  event.currentTarget.style.background = "transparent";
                }}
              >
                {String(option)}
              </div>
            ))
          ) : search.trim() !== "" ? (
            <div
              onMouseDown={(event) => {
                event.preventDefault();
                handleSelect(search.trim());
              }}
              style={{
                padding: "12px",
                color: "#38BDF8",
                fontSize: "13px",
                cursor: "pointer",
                textAlign: "left",
              }}
            >
              ✓ Use &ldquo;{search.trim()}&rdquo; (custom input)
            </div>
          ) : (
            <div
              style={{
                padding: "12px",
                color: "var(--muted-text)",
                fontSize: "13px",
                textAlign: "center",
              }}
            >
              No options found (type to enter custom value)
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default SearchableDropdown;