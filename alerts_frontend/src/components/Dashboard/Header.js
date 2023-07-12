import React from 'react';

const Header = ({ setIsAdding }) => {
  return (
    <header className="header-container">
      <h1 className="header-title">Alerts Dashboard</h1>
      <div className="header-button-container">
        <button className="add-button" onClick={() => setIsAdding(true)}>
          {/* <span className="add-button-icon">+</span>  */}
          Add Alert
        </button>
      </div>
    </header>
  );
};

export default Header;
