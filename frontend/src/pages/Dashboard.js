import React, { useState, useEffect } from "react";
import styles from "../components/Dashboard.module.css";
import { Link, useLocation } from "react-router-dom";
import { API_URL } from "../config";
import { Line, Pie, Bar } from "react-chartjs-2";
import { Chart as ChartJS, LineElement, PointElement, LinearScale, Title, Tooltip, Legend, CategoryScale, ArcElement } from "chart.js";

// Chart.js のコンポーネントを登録
ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend, ArcElement);

const Dashboard = () => {
	const location = useLocation();
	const queryParams = new URLSearchParams(location.search);
	const username = queryParams.get("user");
	
	// Get the name, age, gender from database
	const name = "Michael Jackson";
	const age = 66;
	const gender = "Male";

	// 折れ線グラフのデータ
	const lineData = {
		labels: ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00"],
		datasets: [
			{
				label: "Happy",
				data: [80, 85, 78, 90, 75, 88],
				borderColor: "yellow",
				backgroundColor: "rgba(255, 255, 0, 0.2)",
				tension: 0.4,
			},
			{
				label: "Sad",
				data: [20, 30, 40, 35, 25, 15],
				borderColor: "blue",
				backgroundColor: "rgba(0, 0, 255, 0.2)",
				tension: 0.4,
			},
			{
				label: "Angry",
				data: [10, 15, 20, 25, 30, 20],
				borderColor: "red",
				backgroundColor: "rgba(255, 0, 0, 0.2)",
				tension: 0.4,
			},
			{
				label: "Calm",
				data: [70, 65, 80, 75, 85, 90],
				borderColor: "green",
				backgroundColor: "rgba(0, 255, 0, 0.2)",
				tension: 0.4,
			},
			{
				label: "Fear",
				data: [5, 10, 15, 20, 25, 30],
				borderColor: "purple",
				backgroundColor: "rgba(128, 0, 128, 0.2)",
				tension: 0.4,
			},
		],
	};

	// Smiling Data
	
	// 円グラフのデータ
	const pieData = {
		labels: ["Smiling", "Not Smiling"],
		datasets: [
			{
				data: [72, 28],
				backgroundColor: ["orange", "lightgray"],
			},
		],
	};

	// Speed Data

	// 棒グラフのデータ
	const barData = {
		labels: ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00"],
		datasets: [
			{
				label: "Speaking Speed (WPM)",
				data: [120, 150, 130, 140, 110, 160],
				backgroundColor: "rgba(54, 162, 235, 0.6)",
				borderColor: "blue",
				borderWidth: 1,
			},
		],
	};

	// Question from database
	const [questions, setData] = useState([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);

	// useEffect(() => {
    //     // APIからデータを取得
    //     fetch(`${API_URL}/api/db/sql/Question`)
    //         .then((response) => {
    //             if (!response.ok) {
    //                 throw new Error("Network response was not ok");
    //             }
    //             return response.json();
    //         })
    //         .then((questions) => {
    //             setData(questions);
    //             setLoading(false);
    //         })
    //         .catch((error) => {
    //             console.error("Error fetching data:", error);
    //             setError(error.message);
    //             setLoading(false);
    //         });
    // }, []);

    // if (loading) {
    //     return <div>Loading...</div>;
    // }

    // if (error) {
    //     return <div>Error: {error}</div>;
    // }

	return (
		<div className={styles["page-container"]}>
			<div className={styles.userinfo}>
				<h1 className={styles.title}>Dashboard</h1>
				<div className={styles.info}>
					{name && <p>Name: {name}</p>}
					{age && <p>Age: {age}</p>}
					{gender && <p>Gender: {gender}</p>}
				</div>
			</div>
			<h2 className={styles.title2}>Question: What is the concern or problem that brought you here?</h2>
			{/* {questions && <h2 className={styles.title2}>Question: {questions}</h2>} */}
			<div className={styles["graphs-container"]}>
				{/* 折れ線グラフ */}
				<div className={styles["line-graph"]}>
					<h2>Emotion Trend</h2>
					<Line data={lineData} options={{ responsive: true, scales: { y: { min: 0, max: 100 } } }} />
				</div>
				{/* 円グラフ */}
				<div className={styles["pie-graph"]}>
					<h2>Smile Probability</h2>
					<Pie data={pieData} />
				</div>
				{/* 棒グラフ */}
				{/* <div className={styles["bar-chart"]}>
					<h2>Speaking Speed Over Time</h2>
					<Bar
						data={barData}
						options={{
							responsive: true,
							scales: {
								y: { min: 0, max: 200, title: { display: true, text: "Words Per Minute (WPM)" } }, // y軸: スピード
								x: { title: { display: true, text: "Time" } }, // x軸: 時間
							},
							plugins: {
								legend: { display: false }, // ラベル非表示
							},
						}}
					/>
				</div> */}
			</div>
			{/* Counsellorじゃなかったら表示する */}
			<div className={styles.summary}>
				<h2>Summary</h2>
				<textarea id="summary" name="summary">
				At w3schools.com you will learn how to make a website. They offer free tutorials in all web development technologies.
				</textarea>
			</div>
			<div className={styles.arrow}>
			<Link to="/talk" className={styles.prevButton}>
				<img src="/arrow_left.png" alt="Previous" className={styles.prev} />
			</Link>
			<Link to="/talk" className={styles.nextButton}>
				<img src="/arrow_right.png" alt="Next" className={styles.next} />
			</Link>
			</div>
		</div>
	);
};

export default Dashboard;
