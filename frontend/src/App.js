import { BrowserRouter } from "react-router-dom";
import AppRoutes from "./routes/index";
import Navbar from "./components/Navbar";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <AppRoutes />
    </BrowserRouter>
  );
}

export default App;
