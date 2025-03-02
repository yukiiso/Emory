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
				data: [60, 70, 65, 80, 85, 90],
				borderColor: "yellow",
				backgroundColor: "rgba(255, 255, 0, 0.2)",
				tension: 0.4,
			},
			{
				label: "Sad",
				data: [25, 35, 45, 50, 40, 30],
				borderColor: "blue",
				backgroundColor: "rgba(0, 0, 255, 0.2)",
				tension: 0.4,
			},
			{
				label: "Angry",
				data: [15, 20, 30, 35, 40, 25],
				borderColor: "red",
				backgroundColor: "rgba(255, 0, 0, 0.2)",
				tension: 0.4,
			},
			{
				label: "Calm",
				data: [50, 55, 60, 70, 75, 85],
				borderColor: "green",
				backgroundColor: "rgba(0, 255, 0, 0.2)",
				tension: 0.4,
			},
			{
				label: "Fear",
				data: [10, 15, 25, 30, 35, 40],
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
				data: [84, 16],
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

	useEffect(() => {
        // APIからデータを取得
        fetch(`${API_URL}/api/db/sql/Question`)
			.then((response) => {
				if (!response.ok) {
					throw new Error("Network response was not ok");
				}
				return response.json();
			})
			.then((data) => {
				console.log("Fetched data:", data);

				if (data && data.questions && data.questions.length > 0) {
					setData(data.questions);
					console.log(data.questions[0].id);
					setLoading(false);
				} else {
					console.error("No questions found in the response");
					setLoading(false);
				}
			})
			.catch((error) => {
				console.error("Error fetching data:", error);
				setError(error.message);
				setLoading(false);
			});
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

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
			<h2 className={styles.title2}>Question: {questions && questions.length > 0 ? questions[1].content : 'Loading...'}</h2>
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
			</div>
			{/* Counsellorじゃなかったら表示する */}
			<div className={styles.summary}>
				<h2>Summary</h2>
				<textarea id="summary" name="summary">
				This issue is impacting my life significantly as I'm finding it hard to maintain motivation and keep up with deadlines. I feel constantly drained, both mentally and physically. My relationships are also affected, as I am less present and have little energy left for socializing or pursuing hobbies.
				</textarea>
			</div>
			<div className={styles.arrow}>
			<Link to="/dash" className={styles.prevButton}>
				<img src="/arrow_left.png" alt="Previous" className={styles.prev} />
			</Link>
			<Link to="/dash3" className={styles.nextButton}>
				<img src="/arrow_right.png" alt="Next" className={styles.next} />
			</Link>
			</div>
		</div>
	);
};

export default Dashboard;
