import React, { useState } from "react";

const UploadWidget: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setStatus("Uploading...");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });
      if (res.ok) {
        setStatus("Upload successful!");
      } else {
        setStatus("Upload failed.");
      }
    } catch (err) {
      setStatus("Error during upload.");
    }
  };

  return (
    <div style={{ margin: "1em 0" }}>
      <input type="file" onChange={handleChange} />
      <button onClick={handleUpload} disabled={!file} style={{ marginLeft: 8 }}>
        Upload
      </button>
      <div>{status}</div>
    </div>
  );
};

export default UploadWidget;
