import React, { useEffect, useState } from 'react';
import { MDBTable, MDBTableBody, MDBTableHead } from 'mdbreact';
import axios from 'axios';

const TableComponent = () => {
    const [tableData, setTableData] = useState([]);
  
    // Fetch data from the API
    useEffect(() => {
      axios.get('http://localhost:8000/alert/')
        .then(response => {
          setTableData(response.data.results);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    }, []);

    return (
        <MDBTable>
          <MDBTableHead>
            <tr>
              <th>ID</th>
              <th>Email</th>
              <th>Keywords</th>
              <th>Frequency (in minutes)</th>
            </tr>
          </MDBTableHead>
          <MDBTableBody>
            {tableData.map((item, index) => (
              <tr key={index}>
                <td>{item.id}</td>
                <td>{item.email}</td>
                <td>{item.keywords}</td>
                <td>{item.frequency}</td>
              </tr>
            ))}
          </MDBTableBody>
        </MDBTable>
      );
}

export default TableComponent;