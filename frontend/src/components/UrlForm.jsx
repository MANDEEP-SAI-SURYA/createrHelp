import { useState } from "react";
import { processYoutube } from "../api";

function UrlForm() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleProcess = async () => {
    if (!youtubeUrl) return;

    setLoading(true);

    try {
      await processYoutube(youtubeUrl);
      alert("Video processed successfully!");
      setYoutubeUrl("");
    } catch (err) {
      console.error(err);
      alert("Error processing video");
    }

    setLoading(false);
  };

  return (
    <div style={{ border: "1px solid #ddd", padding: "20px", width: "500px", borderRadius: "10px" }}>
      <h2>Video Sources</h2>

      <input
        type="text"
        placeholder="YouTube URL"
        value={youtubeUrl}
        onChange={(e) => setYoutubeUrl(e.target.value)}
        style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
      />

      <button onClick={handleProcess} disabled={loading}>
        {loading ? "Processing..." : "Process Video"}
      </button>
    </div>
  );
}

export default UrlForm;