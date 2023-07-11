import React from 'react';
import { MDBDataTable } from 'mdbreact';
import { getItems } from './api';

const DatatablePage = () => {
  const response = getItems();
  const data = {
    columns: [
      {
        label: 'Alert ID',
        field: 'alert_id',
        sort: 'asc',
        width: 150
      },
      {
        label: 'Email',
        field: 'email',
        sort: 'asc',
        width: 270
      },
      {
        label: 'Keywords',
        field: 'keywords',
        sort: 'asc',
        width: 400
      },
      {
        label: 'Frequency (in minutes)',
        field: 'frequency',
        sort: 'asc',
        width: 100
      },
    ],
    rows: response
  };

  return (
    <MDBDataTable
      striped
      bordered
      small
      data={data}
    />
  );
}


export default DatatablePage;
