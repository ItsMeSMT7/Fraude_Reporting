import React from 'react';
import ReportForm from './components/ReportForm';
import AllReports from './pages/AllReports';

function App() {
  return (
    <div className="App">
      <h2>Fraud Report System</h2>
      <ReportForm />
      <hr />
      <AllReports />
    </div>
  );
}

export default App;
