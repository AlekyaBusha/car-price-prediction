/**
 * Pagination.jsx
 * Reusable pagination component
 */

import "../styles/Pagination.css";

export default function Pagination({
  currentPage,
  totalPages,
  onPageChange,
  itemsPerPage,
  totalItems,
}) {
  if (totalPages <= 1) return null;

  const startItem = (currentPage - 1) * itemsPerPage + 1;
  const endItem = Math.min(currentPage * itemsPerPage, totalItems);

  return (
    <div className="pagination-container">
      <div className="pagination-info">
        <span className="info-text">
          Showing {startItem} to {endItem} of {totalItems} variants
        </span>
      </div>

      <div className="pagination-controls">
        <button
          className="pagination-btn"
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          aria-label="Previous page"
        >
          ← Previous
        </button>

        <div className="page-numbers">
          {Array.from({ length: totalPages }, (_, i) => {
            const pageNum = i + 1;
            // Show first page, last page, current page, and pages around current
            const showPage =
              pageNum === 1 ||
              pageNum === totalPages ||
              Math.abs(pageNum - currentPage) <= 1;

            if (pageNum > 1 && !showPage && i > 0) {
              const prevNum = i;
              const nextNum = i + 2;
              const prevShow =
                prevNum === 1 ||
                prevNum === totalPages ||
                Math.abs(prevNum - currentPage) <= 1;
              const nextShow =
                nextNum === 1 ||
                nextNum === totalPages ||
                Math.abs(nextNum - currentPage) <= 1;

              if (prevShow && !nextShow) {
                return (
                  <span key={`ellipsis-${i}`} className="ellipsis">
                    ...
                  </span>
                );
              }
              return null;
            }

            if (!showPage) return null;

            return (
              <button
                key={pageNum}
                className={`page-number ${
                  pageNum === currentPage ? "active" : ""
                }`}
                onClick={() => onPageChange(pageNum)}
                aria-label={`Go to page ${pageNum}`}
                aria-current={pageNum === currentPage ? "page" : undefined}
              >
                {pageNum}
              </button>
            );
          })}
        </div>

        <button
          className="pagination-btn"
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          aria-label="Next page"
        >
          Next →
        </button>
      </div>
    </div>
  );
}
