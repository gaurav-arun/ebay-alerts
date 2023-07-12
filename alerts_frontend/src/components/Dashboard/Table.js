import React, { useState } from 'react';
import Pagination from './Pagination';

const Table = ({ alerts, alertsCount, handleEdit, handleDelete, fetchAlerts }) => {
  const itemsPerPage = 5;
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = alertsCount ? Math.ceil(alertsCount / itemsPerPage) : 0;

  const handlePageChange = (page) => {
    setCurrentPage(page);
    fetchAlerts(page);
  };

  return (
    <div className="contain-table">
      <table className="striped-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Search Phrase</th>
            <th>Frequency</th>
            <th colSpan={2} className="text-center">
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          {alerts.length > 0 ? (
            alerts.map((alert) => (
              <tr key={alert.id} >
                <td>{alert.id}</td>
                <td>{alert.email}</td>
                <td>{alert.keywords}</td>
                <td>{alert.frequency}</td>
                <td className="text-center">
                  <button
                    onClick={() => handleEdit(alert.id)}
                    className="button muted-button"
                  >
                    Edit
                  </button>
                </td>
                <td className="text-center">
                  <button
                    onClick={() => handleDelete(alert.id)}
                    className="button muted-button"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr key='no-alerts'>
              <td colSpan={7}>No Alerts</td>
            </tr>
          )}
        </tbody>
      </table>
      {!!totalPages && <Pagination
        currentPage={currentPage}
        alertsCount={alertsCount}
        totalPages={totalPages}
        onPageChange={handlePageChange}
        fetchAlerts={fetchAlerts}
      />}
    </div>
  );
};

export default Table;
