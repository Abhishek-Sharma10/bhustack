import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import Landing from "./pages/Landing";
import ParcelProfile from "./pages/ParcelProfile";
import ServiceRequest from "./pages/ServiceRequest";
import ApplicationTracking from "./pages/ApplicationTracking";
import AdminDashboard from "./pages/AdminDashboard";
import InteropDemo from "./pages/InteropDemo";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/profile/:ulpin" element={<ParcelProfile />} />
        <Route path="/services" element={<ServiceRequest />} />
        <Route path="/tracking" element={<ApplicationTracking />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/interop" element={<InteropDemo />} />
      </Routes>
    </BrowserRouter>
  );
}
