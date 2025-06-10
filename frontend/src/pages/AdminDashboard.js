import React, { useEffect, useState } from "react";

export default function AdminDashboard() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/reports")
      .then((res) => res.json())
      .then((data) => setReports(data))
      .catch((err) => console.error("Error fetching reports:", err));
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <h2 className="text-2xl font-bold mb-6 text-center">🧾 Submitted Fraud Reports</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {reports.map((report) => (
          <div key={report.id} className="bg-white rounded-xl shadow-md p-4 border">
            <p><strong>Name:</strong> {report.victim_name}</p>
            <p><strong>Email:</strong> {report.email}</p>
            <p><strong>Fraud Type:</strong> {report.fraud_type}</p>
            <p><strong>Payment Method:</strong> {report.payment_method}</p>
            <p><strong>Fraud Contact:</strong> {report.fraud_contact}</p>
            <p><strong>Bank Details:</strong> {report.fraud_bank}</p>
            <p><strong>UTR Number:</strong> {report.utr_number}</p>
            <p><strong>Submitted At:</strong> {new Date(report.submitted_at).toLocaleString()}</p>

            {/* Proof Files */}
            {["screenshot_path", "chat_proof_path", "payment_proof_path", "call_recording_path"].map((key) =>
              report[key] ? (
                <a
                  key={key}
                  href={`http://localhost:5000/uploads/${report[key]}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 underline block mt-1"
                >
                  View {key.replace("_path", "").replace("_", " ")}
                </a>
              ) : null
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
