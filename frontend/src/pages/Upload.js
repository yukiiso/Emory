import React, { useState } from 'react';

const UploadForm = () => {
  const [video, setVideo] = useState(null);
  const [audio, setAudio] = useState(null);
  const [username, setUsername] = useState('');
  const [qid, setQid] = useState('');

  const handleVideoChange = (e) => {
    setVideo(e.target.files[0]);
  };

  const handleAudioChange = (e) => {
    setAudio(e.target.files[0]);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === 'username') {
      setUsername(value);
    } else if (name === 'qid') {
      setQid(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('video', video);
    formData.append('audio', audio);
    formData.append('username', username);
    formData.append('qid', qid);

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });
      const result = await response.json();
      if (response.ok) {
        alert('Files uploaded successfully');
      } else {
        alert(`Error: ${result.error}`);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      alert('File upload failed');
    }
  };

  return (
    <div>
      <h1>Upload Video and Audio</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="video">Upload Video:</label>
          <input
            type="file"
            id="video"
            name="video"
            accept="video/*"
            onChange={handleVideoChange}
            required
          />
        </div>
        <div>
          <label htmlFor="audio">Upload Audio:</label>
          <input
            type="file"
            id="audio"
            name="audio"
            accept="audio/*"
            onChange={handleAudioChange}
            required
          />
        </div>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={username}
            onChange={handleInputChange}
            required
          />
        </div>
        <div>
          <label htmlFor="qid">QID:</label>
          <input
            type="text"
            id="qid"
            name="qid"
            value={qid}
            onChange={handleInputChange}
            required
          />
        </div>
        <div>
          <button type="submit">Upload</button>
        </div>
      </form>
    </div>
  );
};

export default UploadForm;
