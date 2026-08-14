import { useEffect, useState } from "react";
import { fetchBrands } from "../services/api";

function CarForm() {
  const [brands, setBrands] = useState([]);
  const [selectedBrand, setSelectedBrand] = useState("");

  useEffect(() => {
    async function loadBrands() {
      try {
        const data = await fetchBrands();

        // Handles both:
        // ["Maruti", "Hyundai"]
        // and { brands: [...] }
        if (Array.isArray(data)) {
          setBrands(data);
        } else if (Array.isArray(data.brands)) {
          setBrands(data.brands);
        } else {
          console.error("Unexpected response:", data);
        }
      } catch (err) {
        console.error("Failed to load brands:", err);
      }
    }

    loadBrands();
  }, []);

  return (
    <div
      style={{
        background: "white",
        padding: "40px",
        borderRadius: "16px",
        boxShadow: "0 6px 20px rgba(0,0,0,.08)",
      }}
    >
      <h2>🚘 Vehicle Details</h2>

      <div style={{ marginTop: "20px" }}>
        <label>
          <strong>Brand</strong>
        </label>

        <br />

        <select
          value={selectedBrand}
          onChange={(e) => setSelectedBrand(e.target.value)}
          style={{
            marginTop: "8px",
            width: "100%",
            padding: "10px",
          }}
        >
          <option value="">Select Brand</option>

          {brands.map((brand) => (
            <option key={brand} value={brand}>
              {brand}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

export default CarForm;