import React, { useState } from 'react';
import axios from 'axios';

const ReportForm = () => {
  const [formData, setFormData] = useState({
    victim_name: '',
    fraud_type: '',
    fraud_description: '',
    fraud_phone: '',
    utr_number: '',
    email: '',
  });
  const [screenshot, setScreenshot] = useState(null);
  const [message, setMessage] = useState('');

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = e => {
    setScreenshot(e.target.files[0]);
  };

  const handleSubmit = async e => {
    e.preventDefault();
    const data = new FormData();
    for (const key in formData) data.append(key, formData[key]);
    if (screenshot) data.append('screenshot', screenshot);

    try {
      const res = await axios.post('http://localhost:5000/api/report', data);
      setMessage(res.data.message);
      setFormData({
        victim_name: '', fraud_type: '', fraud_description: '',
        fraud_phone: '', utr_number: '', email: ''
      });
      setScreenshot(null);
    } catch (err) {
      console.error(err);
      setMessage('Error submitting report');
    }
  };

  return (
    <div className="container mt-4">
      <h2>Report a Fraud</h2>
      {message && <div className="alert alert-info">{message}</div>}
      <form onSubmit={handleSubmit}>
        {['victim_name', 'fraud_type', 'fraud_description', 'fraud_phone', 'utr_number', 'email'].map(field => (
          <div key={field} className="mb-3">
            <input type="text" name={field} placeholder={field.replace('_', ' ')} value={formData[field]} onChange={handleChange} className="form-control" required />
          </div>
        ))}
        <div className="mb-3">
          <input type="file" onChange={handleFileChange} className="form-control" />
        </div>
        <button type="submit" className="btn btn-primary">Submit Report</button>
      </form>
    </div>
  );
};

export default ReportForm;
