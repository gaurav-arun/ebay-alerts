import React, { useEffect, useState } from 'react';
import { MDBDataTable } from 'mdbreact';
// import axios from 'axios';
import { getItems } from './api';

const TableComponent = () => {

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [count, setCount] = useState(0);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await getItems();
      const data = response.results;
      const result_count = response.count;

      setData(data);
      setCount(result_count);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  const columns = [
    {
      label: 'ID',
      field: 'id',
      sort: 'asc',
    },
    {
      label: 'Email',
      field: 'email',
      sort: 'asc',
    },
    {
      label: 'Keywords',
      field: 'keywords',
      sort: 'asc',
    },
    {
      label: 'Frequency (in minutes)',
      field: 'frequency',
      sort: 'asc',
    },
  ];

  const tableData = {
    columns,
    rows: data,
  };

  const totalItems = count;
  const itemsPerPage = 5;
  const totalPages = 100;//Math.ceil(totalItems / itemsPerPage);

  return (
    <MDBDataTable
      striped
      bordered
      hover
      data={tableData}
      paging
      searching={false}
      sortable={false}
      displayEntries={true}
      entries={itemsPerPage}
      entriesOptions={[itemsPerPage, itemsPerPage * 2, itemsPerPage * 3]}
      pagesAmount={totalPages}
      noBottomColumns
      responsive
      info={false}
      theadColor='dark'
      noRecordsFoundLabel='No records found'
    />
  )

    // const [tableData, setTableData] = useState([]);

    // // Fetch data from the API
    // useEffect(() => {
    //   axios.get('http://localhost:8000/alert/')
    //     .then(response => {
    //       setTableData(response.data.results);
    //     })
    //     .catch(error => {
    //       console.error('Error fetching data:', error);
    //     });
    // }, []);

    // return (
    //     // <MDBTable>
    //     //   <MDBTableHead>
    //     //     <tr>
    //     //       <th>ID</th>
    //     //       <th>Email</th>
    //     //       <th>Keywords</th>
    //     //       <th>Frequency (in minutes)</th>
    //     //     </tr>
    //     //   </MDBTableHead>
    //     //   <MDBTableBody>
    //     //     {tableData.map((item, index) => (
    //     //       <tr key={index}>
    //     //         <td>{item.id}</td>
    //     //         <td>{item.email}</td>
    //     //         <td>{item.keywords}</td>
    //     //         <td>{item.frequency}</td>
    //     //       </tr>
    //     //     ))}
    //     //   </MDBTableBody>
    //     // </MDBTable>
    //     <MDBDataTable
    //       striped
    //       bordered
    //       small
    //       data={tableData}
    //     />
    //   );
}

export default TableComponent;
