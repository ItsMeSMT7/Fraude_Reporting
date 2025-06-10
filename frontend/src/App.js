import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import AdminDashboard from "./pages/AdminDashboard"; // or wherever saved

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/admin" element={<AdminDashboard />} />
        {/* other routes */}
      </Routes>
    </Router>
  );
}
