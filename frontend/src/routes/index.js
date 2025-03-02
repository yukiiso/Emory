import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import About from "../pages/About";
import SignIn from "../pages/SignIn";
import SignUp from "../pages/SignUp";
import Talk from "../pages/Talk";
import Record from "../pages/Record";
import Dashboard from "../pages/Dashboard";
import SampleApiData from "../pages/SampleApiData";
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
      <Route path="/dash" element={<Dashboard />} />
      <Route path="/sample-api-data" element={<SampleApiData />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default AppRoutes;
