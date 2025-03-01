import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav>
      <Link to="/">Home</Link> | 
      <Link to="/about">About</Link> | 
      <Link to="/sample-api-data">API Data</Link> | 
      <Link to="/video-upload">Video Upload</Link>
    </nav>
  );
};

export default Navbar;
