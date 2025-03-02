import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import About from "../pages/About";
import SignIn from "../pages/SignIn";
import SignUp from "../pages/SignUp";
import SampleApiData from "../pages/SampleApiData";
import NotFound from "../pages/NotFound";
import Upload from "../pages/Upload";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/sign-in" element={<SignIn />} />
      <Route path="/sign-up" element={<SignUp />} />
      <Route path="/sample-api-data" element={<SampleApiData />} />
      <Route path="*" element={<NotFound />} />
      <Route path="/upload" element={<Upload />} />
      </Routes>
  );
};

export default AppRoutes;
