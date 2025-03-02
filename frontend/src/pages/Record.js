import React, { useState, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { API_URL } from "../config";
import { FFmpeg } from '@ffmpeg/ffmpeg'; // 修正: fetchFileを削除

const ffmpeg = new FFmpeg({ log: true });

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

  const user = [
    { id: 1, username: "john_doe", name: "John Doe" },
  ];

  const question = location.state?.question;

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      videoRef.current.srcObject = stream;
      videoRef.current.play();
      streamRef.current = stream;
      setCameraActive(true);

      mediaRecorderRef.current = new MediaRecorder(stream, { mimeType: "video/webm" });

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          recordedChunks.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(recordedChunks.current, { type: "video/webm" });
        setVideoURL(URL.createObjectURL(blob));
        stopCamera();
      };
    } catch (error) {
      console.error("Error accessing camera:", error);
    }
  };

  const startRecording = () => {
    if (!mediaRecorderRef.current) return;
    recordedChunks.current = [];
    mediaRecorderRef.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    if (!mediaRecorderRef.current) return;
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setCameraActive(false);
  };

  const navigate = useNavigate();

  // 動画をMP4に変換する関数
  const convertWebMToMP4 = async (webmBlob) => {
    await ffmpeg.load(); // ffmpeg.wasmをロード
    const webmFile = new Blob([webmBlob], { type: "video/webm" });
    const webmFileName = "input.webm";
    const mp4FileName = "output.mp4";

    // BlobをFFmpegに書き込む
    ffmpeg.FS("writeFile", webmFileName, new Uint8Array(await webmFile.arrayBuffer()));

    // WebMからMP4に変換
    await ffmpeg.run("-i", webmFileName, mp4FileName);

    // 出力ファイルを取得
    const mp4Data = ffmpeg.FS("readFile", mp4FileName);

    // MP4のBlobを作成
    const mp4Blob = new Blob([mp4Data.buffer], { type: "video/mp4" });
    return mp4Blob;
  };

  const sendVideo = async () => {
    if (!videoURL) return;

    setUploading(true);

    const videoBlob = recordedChunks.current[0];
    const mp4Blob = await convertWebMToMP4(videoBlob); // WebMからMP4に変換

    const formData = new FormData();
    const file = new File([mp4Blob], "video.mp4", { type: "video/mp4" });
    formData.append("video", file);

    try {
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
    <div>
      <div>
        {question && <h1>Question: {question}</h1>}
        <video ref={videoRef} width="700" height="525" autoPlay muted />
        <div>
          {!cameraActive ? (
            <button onClick={startCamera}>Start Camera</button>
          ) : !recording ? (
            <button onClick={startRecording}>Start Recording</button>
          ) : (
            <button onClick={stopRecording}>Stop Recording</button>
          )}
        </div>
        {videoURL && (
          <div>
            <h3>Recorded Video:</h3>
            <video src={videoURL} width="400" height="300" controls />
            <div>
              <button onClick={sendVideo} disabled={uploading}>
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
    </div>
  );
};

export default VideoRecorder;
