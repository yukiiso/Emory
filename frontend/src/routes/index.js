import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import About from "../pages/About";
import SignIn from "../pages/SignIn";
import SignUp from "../pages/SignUp";
import Talk from "../pages/Talk";
import Record from "../pages/Record";
import Search from "../pages/Search";
import Dashboard from "../pages/Dashboard";
import Dashboard2 from "../pages/Dashboard2";
import Dashboard3 from "../pages/Dashboard3";
import Dashboard4 from "../pages/Dashboard4";
import Dashboard5 from "../pages/Dashboard5";
import DashboardC from "../pages/DashboardCouns";
import SampleApiData from "../pages/SampleApiData";
import VideoUpload from "../pages/VideoUpload";
import NotFound from "../pages/NotFound";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/sign-in" element={<SignIn />} />
      <Route path="/sign-up" element={<SignUp />} />
      <Route path="/talk" element={<Talk />} />
      <Route path="/record" element={<Record />} />
      <Route path="/search" element={<Search />} />
      <Route path="/dash" element={<Dashboard />} />
      <Route path="/dash2" element={<Dashboard2 />} />
      <Route path="/dash3" element={<Dashboard3 />} />
      <Route path="/dash4" element={<Dashboard4 />} />
      <Route path="/dash5" element={<Dashboard5 />} />
      <Route path="/dash-c" element={<DashboardC />} />
      <Route path="/sample-api-data" element={<SampleApiData />} />
      <Route path="/video-upload" element={<VideoUpload />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default AppRoutes;
