import React, { useState, useRef } from "react";
import styles from "../components/Record.module.css";
import { useLocation, useNavigate } from "react-router-dom";
import { API_URL } from "../config"; // Flask のエンドポイント

const VideoRecorder = () => {
	const [recording, setRecording] = useState(false);
	const [videoURL, setVideoURL] = useState(null);
	const [cameraActive, setCameraActive] = useState(false);
	const [uploading, setUploading] = useState(false);
	const [videoUploadURL, setVideoUploadURL] = useState(null);

	const mediaRecorderRef = useRef(null);
	const videoRef = useRef(null);
	const recordedChunks = useRef([]);
	const streamRef = useRef(null);
	const location = useLocation();
	const navigate = useNavigate();

	// Assume current user
	const user = [
        { id: 1, username: "john_doe", name: "John Doe" },
    ];

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
				stopCamera(); // 録画停止後にカメラオフ
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

	// ⏹ 録画停止
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

	// 動画を Flask に送信
	const sendVideo = async () => {
		if (!videoURL) return;

		setUploading(true);

		const webmBlob = new Blob(recordedChunks.current, { type: "video/webm" });

		const formData = new FormData();
		const file = new File([webmBlob], "video.webm", { type: "video/webm" });
		formData.append("video", file);

		try {
			// WebM ファイルを Flask に送信
			const response = await fetch(`${API_URL}/api/s3/upload`, {
				method: "POST",
				body: formData,
			});

			const data = await response.json();
			if (response.ok) {
				setVideoUploadURL(data.url);
			} else {
				console.error("Upload failed:", data.error);
			}
		} catch (error) {
			console.error("Error during video upload:", error);
		} finally {
			setUploading(false);
		}

		navigate(`/dash?user=${user[0].username}`);
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
						<button className={styles.buttonDesignRed} onClick={stopRecording}>Stop Recording</button>
					)}
				</div>
				{videoURL && (
					<div>
						<h3>Recorded Video:</h3>
						<video src={videoURL} width="400" height="300" controls />
						{uploading && <p>Uploading...</p>}
						<div className={styles.saveBt}>
							<button className={styles.buttonDesign} onClick={sendVideo} disabled={uploading}>
								{uploading ? "Uploading..." : "Send Video"}
							</button>
						</div>
					</div>
				)}
				{videoUploadURL && (
					<div>
						<h3>Uploaded Video URL:</h3>
						<a href={videoUploadURL} target="_blank" rel="noopener noreferrer">
							{videoUploadURL}
						</a>
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
