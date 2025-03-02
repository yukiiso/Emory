import { useState } from "react";
import { API_URL } from "../config";

const VideoUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage("ファイルを選択してください");
      return;
    }

    const formData = new FormData();
    formData.append("video", selectedFile);

    setUploading(true);
    setMessage("");

    try {
      const response = await fetch(`${API_URL}/api/s3/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setMessage(`アップロード成功: ${data.url}`);
      } else {
        setMessage(`エラー: ${data.error}`);
      }
    } catch (error) {
      setMessage(`通信エラー: ${error.message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h2>動画アップロード</h2>
      <input type="file" accept="video/*" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? "アップロード中..." : "アップロード"}
      </button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default VideoUpload;
