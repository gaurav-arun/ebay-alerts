import React from 'react';

const Pagination = ({ currentPage, totalPages, alertsCount, onPageChange, fetchAlerts }) => {
  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
      fetchAlerts(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages) {
      onPageChange(currentPage + 1);
      fetchAlerts(currentPage + 1);
    }
  };

  return (
    <div className="pagination-container">
      <span className="pagination-info">Total: {alertsCount}</span>
      <button className="pagination-button" onClick={handlePrevious} disabled={currentPage === 1}>
        &lt;
      </button>
      <span className="pagination-page">Page {currentPage} / {totalPages}</span>
      <button className="pagination-button" onClick={handleNext} disabled={currentPage === totalPages}>
       &gt;
      </button>
    </div>
  );
};

export default Pagination;
