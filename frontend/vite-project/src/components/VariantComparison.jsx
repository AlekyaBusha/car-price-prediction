/**
 * VariantComparison.jsx
 * Display and compare variant predictions with sorting and pagination
 */

import { useState, useMemo } from "react";
import VariantCard from "./VariantCard";
import Pagination from "./Pagination";
import LoadingSpinner from "./LoadingSpinner";
import "../styles/VariantComparison.css";

const ITEMS_PER_PAGE = 8;

export default function VariantComparison({ variants = [], loading }) {
  const [currentPage, setCurrentPage] = useState(1);
  const [sortBy, setSortBy] = useState("price"); // 'price' or 'name'
  const [sortOrder, setSortOrder] = useState("asc"); // 'asc' or 'desc'

  // Sort variants based on current sort settings
  const sortedVariants = useMemo(() => {
    if (!variants || variants.length === 0) return [];

    const sorted = [...variants];

    sorted.sort((a, b) => {
      let compareValue = 0;

      if (sortBy === "price") {
        compareValue = a.predicted_price - b.predicted_price;
      } else if (sortBy === "name") {
        const aName = `${a.fuel_type}-${a.transmission_type}`;
        const bName = `${b.fuel_type}-${b.transmission_type}`;
        compareValue = aName.localeCompare(bName);
      } else if (sortBy === "engine") {
        compareValue = (a.engine || 0) - (b.engine || 0);
      }

      return sortOrder === "asc" ? compareValue : -compareValue;
    });

    return sorted;
  }, [variants, sortBy, sortOrder]);

  // Paginate variants
  const totalPages = Math.ceil(sortedVariants.length / ITEMS_PER_PAGE);
  const paginatedVariants = useMemo(() => {
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    return sortedVariants.slice(startIndex, endIndex);
  }, [sortedVariants, currentPage]);

  // Reset to first page when sort changes
  const handleSortChange = (field) => {
    if (sortBy === field) {
      // Toggle sort order if same field clicked
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      // Set new sort field with ascending order
      setSortBy(field);
      setSortOrder("asc");
    }
    setCurrentPage(1);
  };

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    // Scroll to top of variants section
    const container = document.querySelector(".variant-comparison-container");
    if (container) {
      container.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!sortedVariants || sortedVariants.length === 0) {
    return (
      <div className="variant-comparison-container">
        <p className="no-variants-message">
          No variants available. Please select a brand and model to see variants.
        </p>
      </div>
    );
  }

  return (
    <div className="variant-comparison-container">
      <div className="variant-header-section">
        <h3 className="section-title">Available Variants</h3>
        <p className="variant-count">
          {sortedVariants.length} variant{sortedVariants.length !== 1 ? "s" : ""} found
        </p>
      </div>

      {/* Sorting Controls */}
      <div className="sort-controls">
        <span className="sort-label">Sort by:</span>

        <div className="sort-buttons">
          <button
            className={`sort-btn ${sortBy === "price" ? "active" : ""}`}
            onClick={() => handleSortChange("price")}
          >
            Price
            {sortBy === "price" && (
              <span className="sort-indicator">
                {sortOrder === "asc" ? " ↑" : " ↓"}
              </span>
            )}
          </button>

          <button
            className={`sort-btn ${sortBy === "name" ? "active" : ""}`}
            onClick={() => handleSortChange("name")}
          >
            Type
            {sortBy === "name" && (
              <span className="sort-indicator">
                {sortOrder === "asc" ? " ↑" : " ↓"}
              </span>
            )}
          </button>

          <button
            className={`sort-btn ${sortBy === "engine" ? "active" : ""}`}
            onClick={() => handleSortChange("engine")}
          >
            Engine
            {sortBy === "engine" && (
              <span className="sort-indicator">
                {sortOrder === "asc" ? " ↑" : " ↓"}
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Variants Grid */}
      <div className="variants-grid">
        {paginatedVariants.map((variant, index) => {
          // Check if this is the highest priced variant in the entire sorted list
          const isHighest = sortedVariants.length > 0 && 
            variant.predicted_price === Math.max(...sortedVariants.map(v => v.predicted_price || 0));
          
          return (
            <VariantCard
              key={`${variant.fuel_type}-${variant.transmission_type}-${index}`}
              variant={variant}
              index={(currentPage - 1) * ITEMS_PER_PAGE + index + 1}
              isHighest={isHighest}
            />
          );
        })}
      </div>

      {/* Pagination */}
      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={handlePageChange}
        itemsPerPage={ITEMS_PER_PAGE}
        totalItems={sortedVariants.length}
      />
    </div>
  );
}
