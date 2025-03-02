import React, { useState, useRef } from "react";
import styles from "../components/Record.module.css";
import { useLocation } from "react-router-dom";

const VideoRecorder = () => {
	const [recording, setRecording] = useState(false);
	const [videoURL, setVideoURL] = useState(null);
	const [cameraActive, setCameraActive] = useState(false);
	const mediaRecorderRef = useRef(null);
	const videoRef = useRef(null);
	const recordedChunks = useRef([]);
	const streamRef = useRef(null);
	const location = useLocation();

	// Talk.jsから送られてきた質問
    const question = location.state?.question;

	// カメラとマイクを起動
	const startCamera = async () => {
	try {
		const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
		videoRef.current.srcObject = stream;
		videoRef.current.play();
		streamRef.current = stream; // ストリームを保存
		setCameraActive(true);

		// MediaRecorderの設定
		mediaRecorderRef.current = new MediaRecorder(stream, { mimeType: "video/webm" });

		mediaRecorderRef.current.ondataavailable = (event) => {
		if (event.data.size > 0) {
			recordedChunks.current.push(event.data);
		}
		};

		mediaRecorderRef.current.onstop = () => {
		const blob = new Blob(recordedChunks.current, { type: "video/webm" });
		setVideoURL(URL.createObjectURL(blob));

		// ⏹ 録画停止後にカメラとマイクをオフにする
		stopCamera();
		};
	} catch (error) {
			console.error("Error accessing camera:", error);
		}
	};

	// ▶️ 録画開始
	const startRecording = () => {
		if (!mediaRecorderRef.current) return;
		recordedChunks.current = [];
		mediaRecorderRef.current.start();
		setRecording(true);
	};

	// ⏹ 録画停止 & カメラオフ
	const stopRecording = () => {
		if (!mediaRecorderRef.current) return;
		mediaRecorderRef.current.stop();
		setRecording(false);
	};
	
	// カメラとマイクをオフ
	const stopCamera = () => {
		if (streamRef.current) {
			streamRef.current.getTracks().forEach((track) => track.stop()); // カメラ＆マイク停止
			streamRef.current = null;
		}
		setCameraActive(false);
	};

	// ⬇️ 動画をダウンロード
	const sendVideo = () => {
		// TODO: StorageにSave機能追加
	};

	return (
	<div className={styles["page-container"]}>
		<div className={styles.videoSection}>
			{question && <h1>Question: {question}</h1>}
			<video ref={videoRef} width="700" height="525" autoPlay muted />
			<div style={{ marginTop: "10px" }}>
			{!cameraActive ? (
				<button className={styles.buttonDesign} onClick={startCamera}>Start Camera</button>
			) : !recording ? (
				<button className={styles.buttonDesign} onClick={startRecording}>Start Recording</button>
			) : (
				<button className={styles.buttonDesign} onClick={stopRecording}>Stop Recording</button>
			)}
			</div>
			{videoURL && (
			<div>
				<h3>Recorded Video:</h3>
				<video src={videoURL} width="400" height="300" controls />
				<br />
				{/* TODO: DownloadじゃなくてSaveしなきゃいけない */}
				<div className={styles.saveBt}>
					<button className={styles.buttonDesign} onClick={sendVideo}>Send Video</button>
				</div>
			</div>
			)}
		</div>
		<div className={styles.instructionSection}>
			<h2 className={styles.instructions}>How to Use</h2>
			<ol>
				<li>Click "Start Camera" to enable video recording.</li>
				<li>Press "Start Recording" to begin answering the question.</li>
				<li>When finished, click "Stop Recording".</li>
				<li>Your video will be displayed below, and you can check it.</li>
			</ol>
		</div>
	</div>
	);
};

export default VideoRecorder;
