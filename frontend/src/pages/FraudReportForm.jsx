import React from "react";

export default function FraudReportForm() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-red-100 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white shadow-2xl rounded-2xl p-6">
        <h2 className="text-2xl font-bold text-center mb-4 text-red-600">
          Report a Fraud
        </h2>
        <form className="space-y-4">
          <input className="w-full p-2 border rounded" placeholder="Your Full Name" required />
          <input className="w-full p-2 border rounded" type="email" placeholder="Your Email Address" required />
          <input className="w-full p-2 border rounded" type="tel" placeholder="Your Phone Number" required />
          <input className="w-full p-2 border rounded" placeholder="Fraud Type (e.g., UPI, Fake Job, OLX)" required />
          <input className="w-full p-2 border rounded" placeholder="Fraudster Contact / Bank Account / Email" required />
          <textarea className="w-full p-2 border rounded" placeholder="Describe the incident in detail..." rows={4} required></textarea>
          <input className="w-full p-2 border rounded" type="file" multiple />
          <button type="submit" className="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700">
            Submit Report
          </button>
        </form>
      </div>

      <div className="mt-6 text-sm text-center text-gray-500 border-t border-gray-300 pt-4 max-w-2xl">
        <strong>Legal Tip:</strong> We are a third-party platform aimed at assisting victims of online fraud.
        We do not store sensitive data permanently and only forward submitted cases to relevant government agencies
        like{" "}
        <a
          href="https://www.cybercrime.gov.in/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 underline"
        >
          cybercrime.gov.in
        </a>.
      </div>
    </div>
  );
}
