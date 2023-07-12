import React, { useState } from 'react';
import Swal from 'sweetalert2';
import * as alertsService from '../../services';

const AlertForm = ({ title, buttonLabel, alerts, setAlerts, setIsEditing, setIsAdding, selectedAlert }) => {
  const [email, setEmail] = useState(selectedAlert ? selectedAlert.email : '');
  const [keywords, setKeywords] = useState(selectedAlert ? selectedAlert.keywords : '');
  const [frequency, setFrequency] = useState(selectedAlert ? selectedAlert.frequency : '');
  const [emailError, setEmailError] = useState('');
  const [keywordsError, setKeywordsError] = useState('');

  // To differentiate between Add and Edit action
  const isEditAction = !!selectedAlert;
  const setAddOrEditAction = isEditAction ? setIsEditing : setIsAdding;

  const handleKeywordsChange = (e) => {
    const inputKeywords = e.target.value;
    setKeywords(inputKeywords);

    if (!inputKeywords) {
      setKeywordsError('Keywords are required');
    } else if (/[^\w\s]/.test(inputKeywords)) {
      setKeywordsError('Keywords should not contain special characters');
    } else {
      setKeywordsError('');
    }
  };

  const handleEmailChange = (e) => {
    const inputEmail = e.target.value;
    setEmail(inputEmail);

    if (!inputEmail) {
      setEmailError('Email is required');
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(inputEmail)) {
      setEmailError('Invalid email');
    } else {
      setEmailError('');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!email || !keywords || !frequency) {
      const errorMessage =  !frequency ? ' Please select a frequency.': ' Please fill out all fields.';
      return Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: errorMessage,
        showConfirmButton: true,
      });
    }

    let alert = {
      email,
      keywords,
      frequency,
    };

    if (isEditAction) {
      alert = {
        ...alert,
        id: selectedAlert.id,
      };
    }

    const actionPromise = selectedAlert ? alertsService.updateAlert(alert) : alertsService.createAlert(alert);

    actionPromise
      .then(() => {
        setAlerts(alerts);
        setAddOrEditAction(false);

        const successTitle = selectedAlert ? 'Updated!' : 'Added!';
        const successText = selectedAlert ? 'Alert has been updated.' : 'New Alert has been added.';
        Swal.fire({
          icon: 'success',
          title: successTitle,
          text: successText,
          showConfirmButton: false,
          timer: 1500,
        });
      })
      .catch((error) => {
        console.error('Error updating alert:', error);
        throw error;
      });
  };

  return (
    <div className="small-container">
      <form onSubmit={handleSubmit} noValidate>
        <h1>{title}</h1>
        <label htmlFor="email">Email</label>
        <input
          type="email"
          name="email"
          value={email}
          onChange={handleEmailChange}
          className={emailError ? 'error' : ''}
        />
        {emailError && <div className="error-message">{emailError}</div>}
        <label htmlFor="keywords">Search Phrase</label>
        <input
          type="text"
          name="keywords"
          value={keywords}
          onChange={handleKeywordsChange}
          className={keywordsError ? 'error' : ''}
        />
        {keywordsError && <div className="error-message">{keywordsError}</div>}
        <div>
          <label htmlFor="frequency">Frequency (in minutes)</label>
          <select value={frequency} onChange={(e) => setFrequency(e.target.value)}>
            <option value="2" selected>2</option>
            <option value="5">5</option>
            <option value="30">30</option>
          </select>
        </div>
        <div style={{ marginTop: '30px' }}>
          <input type="submit" value={buttonLabel} />
          <input
            style={{ marginLeft: '12px' }}
            className="muted-button"
            type="button"
            value="Cancel"
            onClick={() => {
                setAddOrEditAction(false);
            }}
          />
        </div>
      </form>
    </div>
  );
};

export default AlertForm;
