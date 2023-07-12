import React from 'react';
import AlertForm from './AlertForm.js';

const Add = ({ alerts, setAlerts, setIsAdding }) => {
  return (
    <AlertForm
      title="Add Alert"
      buttonLabel="Add"
      alerts={alerts}
      setAlerts={setAlerts}
      setIsAdding={setIsAdding}
    />
  );
};

export default Add;
