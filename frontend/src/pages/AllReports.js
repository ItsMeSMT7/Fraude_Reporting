import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AllReports = () => {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/api/reports')
      .then(res => setReports(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h3>Submitted Fraud Reports</h3>
      <ul>
        {reports.map((report, index) => (
          <li key={index}>
            <strong>{report.name}</strong> reported <strong>{report.fraudType}</strong> via <strong>{report.phone}</strong><br />
            UTR: {report.utr}<br />
            Description: {report.description}<br />

            {/* Conditionally render the screenshot image if it exists */}
            {report.screenshot && (
              <img
                src={`http://localhost:5000/uploads/${report.screenshot}`}
                alt="Proof"
                width="300"
                style={{ marginTop: "10px" }}
              />
            )}
            <hr />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AllReports;
