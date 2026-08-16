import { useEffect, useRef, useState } from "react";

function SearchableDropdown({
  label,
  options = [],
  value,
  onChange,
  placeholder = "Search...",
  disabled = false,
}) {
  const [search, setSearch] = useState(
    value !== null && value !== undefined
      ? String(value)
      : ""
  );

  const [isOpen, setIsOpen] = useState(false);

  const containerRef = useRef(null);

  // ---------------------------------------------------------
  // Sync selected value when dropdown is closed
  // ---------------------------------------------------------

  useEffect(() => {
    if (!isOpen) {
      setSearch(
        value !== null && value !== undefined
          ? String(value)
          : ""
      );
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

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );
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

    // Clear current value so user can search for another value
    setSearch("");
  }

  // ---------------------------------------------------------
  // Handle typing
  // ---------------------------------------------------------

  function handleSearch(event) {
    const inputValue = event.target.value;

    setSearch(inputValue);

    setIsOpen(true);

    if (inputValue === "") {
      onChange("");
    }
  }

  // ---------------------------------------------------------
  // Select option
  // ---------------------------------------------------------

  function handleSelect(option) {
    setSearch(String(option));

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
      }
    }

    if (event.key === "Escape") {
      setIsOpen(false);

      setSearch(
        value !== null && value !== undefined
          ? String(value)
          : ""
      );
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
        marginTop: "20px",
      }}
    >
      <label>
        <strong>{label}</strong>
      </label>

      <div
        style={{
          position: "relative",
          marginTop: "8px",
        }}
      >
        <input
          type="text"
          value={search}
          placeholder={placeholder}
          disabled={disabled}
          onFocus={handleFocus}
          onChange={handleSearch}
          onKeyDown={handleKeyDown}
            style={{
            width: "100%",
            padding: "12px 40px 12px 12px",
            boxSizing: "border-box",
            border: "1px solid var(--border)",
            borderRadius: "8px",
            fontSize: "15px",
            outline: "none",
            background: disabled
              ? "var(--muted-bg)"
              : "var(--card-bg)",
            color: "var(--text)",
          }}
        />

        <span
          style={{
            position: "absolute",
            right: "12px",
            top: "50%",
            transform: "translateY(-50%)",
            pointerEvents: "none",
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
            background: "var(--card-bg)",
            border: "1px solid var(--border)",
            borderRadius: "8px",
            maxHeight: "220px",
            overflowY: "auto",
            zIndex: 1000,
            boxShadow:
              "0 6px 30px rgba(0,0,0,0.6)",
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
                  padding: "11px 12px",
                  cursor: "pointer",
                  borderBottom:
                    "1px solid rgba(255,255,255,0.02)",
                  fontSize: "15px",
                  color: "var(--text)",
                }}
                onMouseEnter={(event) => {
                  event.currentTarget.style.background =
                    "var(--muted-bg)";
                }}
                onMouseLeave={(event) => {
                  event.currentTarget.style.background =
                    "var(--card-bg)";
                }}
              >
                {String(option)}
              </div>
            ))
          ) : (
            <div
              style={{
                padding: "12px",
                color: "#777",
              }}
            >
              No results found
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default SearchableDropdown;