import React from 'react';
import AlertForm from './AlertForm.js';

const Edit = ({ alerts, selectedAlert, setAlerts, setIsEditing }) => {
  return (
    <AlertForm
      title="Edit Alert"
      buttonLabel="Update"
      alerts={alerts}
      setAlerts={setAlerts}
      setIsEditing={setIsEditing}
      selectedAlert={selectedAlert}
    />
  );
};

export default Edit;
