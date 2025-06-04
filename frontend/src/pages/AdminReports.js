import React, { useEffect, useState } from 'react';
import axios from 'axios';

function AdminReports() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/api/reports') // Flask API
      .then(res => setReports(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="container mt-4">
      <h2>Submitted Fraud Reports</h2>
      <table className="table table-bordered">
        <thead>
          <tr>
            <th>Victim Name</th>
            <th>Fraud Type</th>
            <th>UTR</th>
            <th>Phone</th>
            <th>Submitted</th>
          </tr>
        </thead>
        <tbody>
          {reports.map((r, i) => (
            <tr key={i}>
              <td>{r.victim_name}</td>
              <td>{r.fraud_type}</td>
              <td>{r.utr_number}</td>
              <td>{r.fraud_phone}</td>
              <td>{new Date(r.submitted_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminReports;
