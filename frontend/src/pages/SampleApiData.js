import { useState, useEffect } from "react";
import { API_URL } from "../config";

const SampleApiData = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log(`Fetching data from: ${API_URL}/api/health`);

    fetch(`${API_URL}/api/health`)
      .then((response) => {
        console.log("Response status:", response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((json) => {
        console.log("Fetched data:", json);
        setData(json); 
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
        setError(err.message);
      });
  }, []);

  return (
    <div>
      <h1>API Data Page</h1>
      {error && <p style={{ color: "red" }}>Error: {error}</p>}
      {data ? (
        <div>
          <p>{data.message}</p>
        </div>
      ) : !error ? (
        <p>Loading...</p>
      ) : null}
    </div>
  );
};

export default SampleApiData;
