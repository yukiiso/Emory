import React from "react";
import styles from "../components/Dashboard.module.css";
import { Line, Pie } from "react-chartjs-2";
import { Chart as ChartJS, LineElement, PointElement, LinearScale, Title, Tooltip, Legend, CategoryScale, ArcElement } from "chart.js";

// Chart.js のコンポーネントを登録
ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend, ArcElement);

const Dashboard = () => {
  // 折れ線グラフのデータ
  const lineData = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    datasets: [
      {
        label: "Sales",
        data: [10, 30, 50, 40, 70, 100],
        borderColor: "blue",
        backgroundColor: "rgba(0, 0, 255, 0.2)",
        tension: 0.4,
      },
    ],
  };

  // 円グラフのデータ
  const pieData = {
    labels: ["Apple", "Banana", "Cherry"],
    datasets: [
      {
        data: [40, 30, 30],
        backgroundColor: ["red", "yellow", "pink"],
      },
    ],
  };

  return (
    <div className={styles["page-container"]}>
        <h1 className={styles.title}>Dashboard</h1>
        <div className={styles["graphs-container"]}>
            {/* 折れ線グラフ */}
            <div className={styles["line-graph"]}>
                <h2>Sales Trend</h2>
                <Line data={lineData} />
            </div>
            {/* 円グラフ */}
            <div className={styles["pie-graph"]}>
                <h2>Product Share</h2>
                <Pie data={pieData} />
            </div>
        </div>
        {/* Counsellorじゃなかったら表示する */}
        <div className={styles.summary}>
            <h2>Summary</h2>
            <textarea id="summary" name="summary">
            At w3schools.com you will learn how to make a website. They offer free tutorials in all web development technologies.
            </textarea>
        </div>
    </div>
  );
};

export default Dashboard;
