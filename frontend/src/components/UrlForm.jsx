import { useState } from "react";

function UrlForm() {

  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [instagramUrl, setInstagramUrl] = useState("");

  return (
    <div
      style={{
        border: "1px solid #ddd",
        padding: "20px",
        width: "500px",
        borderRadius: "10px",
      }}
    >
      <h2>Video Sources</h2>

      <input
        type="text"
        placeholder="YouTube Shorts URL"
        value={youtubeUrl}
        onChange={(e) => setYoutubeUrl(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px",
        }}
      />

      <input
        type="text"
        placeholder="Instagram Reel URL"
        value={instagramUrl}
        onChange={(e) => setInstagramUrl(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
        }}
      />

      <br /><br />

      <button
        style={{
          padding: "10px 20px",
          cursor: "pointer",
        }}
      >
        Process Videos
      </button>
    </div>
  );
}

export default UrlForm;