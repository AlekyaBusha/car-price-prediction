/**
 * VariantComparison.jsx
 * Display and compare variant predictions with sorting, pagination,
 * and the "Compare All Variants" trigger button located in the component header.
 */

import { useState, useMemo } from "react";
import VariantCard from "./VariantCard";
import Pagination from "./Pagination";
import LoadingSpinner from "./LoadingSpinner";
import "../styles/VariantComparison.css";

const ITEMS_PER_PAGE = 8;

export default function VariantComparison({
  variants = [],
  loading = false,
  onCompareAllVariants,
  isComparing = false,
  hasModelSelected = true,
}) {
  const [currentPage, setCurrentPage] = useState(1);
  const [sortBy, setSortBy] = useState("price"); // 'price', 'name', 'engine'
  const [sortOrder, setSortOrder] = useState("desc"); // default to highest price first

  // Sort variants based on current sort settings
  const sortedVariants = useMemo(() => {
    if (!variants || variants.length === 0) return [];

    const sorted = [...variants];

    sorted.sort((a, b) => {
      let compareValue = 0;

      if (sortBy === "price") {
        compareValue = (a.predicted_price || 0) - (b.predicted_price || 0);
      } else if (sortBy === "name") {
        const aName = String(a.variant || a.model || "").toLowerCase();
        const bName = String(b.variant || b.model || "").toLowerCase();
        compareValue = aName.localeCompare(bName);
      } else if (sortBy === "engine") {
        compareValue = (Number(a.engine) || 0) - (Number(b.engine) || 0);
      }

      return sortOrder === "asc" ? compareValue : -compareValue;
    });

    return sorted;
  }, [variants, sortBy, sortOrder]);

  // Paginate variants (8 per page)
  const totalPages = Math.ceil(sortedVariants.length / ITEMS_PER_PAGE);
  const paginatedVariants = useMemo(() => {
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    return sortedVariants.slice(startIndex, endIndex);
  }, [sortedVariants, currentPage]);

  const handleSortChange = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortBy(field);
      setSortOrder(field === "price" ? "desc" : "asc");
    }
    setCurrentPage(1);
  };

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    const container = document.querySelector(".variant-comparison-container");
    if (container) {
      container.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  const maxPrice = useMemo(() => {
    if (!variants || variants.length === 0) return 0;
    return Math.max(...variants.map((v) => v.predicted_price || 0));
  }, [variants]);

  return (
    <div className="variant-comparison-container">
      {/* Top Header with Title, Count and Compare All Variants Button */}
      <div className="variant-header-section">
        <div className="variant-title-group">
          <h3 className="section-title">Available Variants</h3>
          <p className="variant-count">
            {variants.length > 0
              ? `${variants.length} variant${variants.length !== 1 ? "s" : ""} found`
              : "Compare trims & specs for this vehicle"}
          </p>
        </div>

        {onCompareAllVariants && (
          <button
            type="button"
            className="btn-compare-variants"
            onClick={onCompareAllVariants}
            disabled={isComparing || loading || !hasModelSelected}
          >
            {isComparing || loading ? (
              <>
                <span className="btn-spinner" /> Loading Variants...
              </>
            ) : (
              "🔍 Compare All Variants"
            )}
          </button>
        )}
      </div>

      {loading ? (
        <div className="variant-loading-box">
          <LoadingSpinner />
        </div>
      ) : !sortedVariants || sortedVariants.length === 0 ? (
        <div className="no-variants-message">
          <p>No matching variants available for this selection.</p>
          {onCompareAllVariants && (
            <button
              type="button"
              className="btn-compare-prompt"
              onClick={onCompareAllVariants}
              disabled={!hasModelSelected}
            >
              Click &ldquo;Compare All Variants&rdquo; to search trims
            </button>
          )}
        </div>
      ) : (
        <>
          {/* Sorting Controls */}
          <div className="sort-controls">
            <span className="sort-label">Sort by:</span>

            <div className="sort-buttons">
              <button
                type="button"
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
                type="button"
                className={`sort-btn ${sortBy === "name" ? "active" : ""}`}
                onClick={() => handleSortChange("name")}
              >
                Variant Name
                {sortBy === "name" && (
                  <span className="sort-indicator">
                    {sortOrder === "asc" ? " ↑" : " ↓"}
                  </span>
                )}
              </button>

              <button
                type="button"
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

          {/* 4x2 Desktop Responsive Grid */}
          <div className="variants-grid">
            {paginatedVariants.map((variant, index) => {
              const isHighest =
                maxPrice > 0 && variant.predicted_price === maxPrice;

              return (
                <VariantCard
                  key={`${variant.variant}-${variant.fuel_type}-${variant.transmission_type}-${index}`}
                  variant={variant}
                  index={(currentPage - 1) * ITEMS_PER_PAGE + index + 1}
                  isHighest={isHighest}
                />
              );
            })}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={handlePageChange}
              itemsPerPage={ITEMS_PER_PAGE}
              totalItems={sortedVariants.length}
            />
          )}
        </>
      )}
    </div>
  );
}
