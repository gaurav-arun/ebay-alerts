import React, { useState, useEffect } from 'react';
import Swal from 'sweetalert2';

import Header from './Header';
import Table from './Table';
import Add from './Add';
import Edit from './Edit';

import * as alertsService from '../../services';


const Dashboard = () => {
  const [alerts, setAlerts] = useState([]);
  const [alertsCount, setAlertsCount] = useState(0);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [isAdding, setIsAdding] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    fetchAlerts();
  }, [isEditing, isAdding, isDeleting])

  const fetchAlerts = async (page=1) => {
    try {
      const alertsResponse = await alertsService.fetchAlerts(page);
      setAlerts(alertsResponse?.results);
      setAlertsCount(alertsResponse?.count);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    }
  };

  const handleEdit = id => {
    const [alert] = alerts.filter(alert => alert.id === id);

    setSelectedAlert(alert);
    setIsEditing(true);
  };

  const handleDelete = id => {
    Swal.fire({
      icon: 'warning',
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      showCancelButton: true,
      confirmButtonText: 'Yes, delete it!',
      cancelButtonText: 'No, cancel!',
    }).then(result => {
      if (result.value) {
        setIsDeleting(true);

        alertsService.deleteAlert(id).then( () => {
          setIsDeleting(false);

          Swal.fire({
            icon: 'success',
            title: 'Deleted!',
            text: 'Alert has been deleted.',
            showConfirmButton: false,
            timer: 1500,
          });
        }).catch( (error) => {
          console.error('Error deleting alert:', error);
          throw error;
        })
      }
    });
  };

  return (
    <div className="container">
      {!isAdding && !isEditing && (
        <>
          <Header
            setIsAdding={setIsAdding}
          />
          <Table
            alerts={alerts}
            handleEdit={handleEdit}
            handleDelete={handleDelete}
            fetchAlerts={fetchAlerts}
            alertsCount={alertsCount}
          />
        </>
      )}
      {isAdding && (
        <Add
          alerts={alerts}
          setAlerts={setAlerts}
          setIsAdding={setIsAdding}
        />
      )}
      {isEditing && (
        <Edit
          alerts={alerts}
          selectedAlert={selectedAlert}
          setAlerts={setAlerts}
          setIsEditing={setIsEditing}
        />
      )}
    </div>
  );
};

export default Dashboard;
