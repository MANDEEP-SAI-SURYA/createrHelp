import { useState } from "react";
import {processYoutube,processInstagram,} from "../api";

function UrlForm() {
  const [youtubeUrl, setYoutubeUrl] =useState("");

  const [instagramUrl, setInstagramUrl] =useState("");

  const [loading, setLoading] =useState(false);

  const handleProcess = async () => {
    if (!youtubeUrl) return;

    setLoading(true);

    try {
      await processYoutube(youtubeUrl);

      alert(
        "YouTube video processed successfully!"
      );

      setYoutubeUrl("");

    } catch (err) {

      console.error(err);

      alert(
        "Error processing YouTube video"
      );
    }

    setLoading(false);
  };

  const handleInstagramProcess =
    async () => {

      if (!instagramUrl) return;

      setLoading(true);

      try {

        await processInstagram(
          instagramUrl
        );

        alert(
          "Instagram Reel processed successfully!"
        );

        setInstagramUrl("");

      } catch (err) {

        console.error(err);

        alert(
          "Error processing Instagram Reel"
        );
      }

      setLoading(false);
    };

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

      {/* YouTube Section */}

      <h3>YouTube</h3>

      <input
        type="text"
        placeholder="YouTube URL"
        value={youtubeUrl}
        onChange={(e) =>
          setYoutubeUrl(e.target.value)
        }
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px",
        }}
      />

      <button
        onClick={handleProcess}
        disabled={loading}
      >
        {loading
          ? "Processing..."
          : "Process Video"}
      </button>

      <hr
        style={{
          margin: "20px 0",
        }}
      />

      {/* Instagram Section */}

      <h3>Instagram</h3>

      <input
        type="text"
        placeholder="Instagram Reel URL"
        value={instagramUrl}
        onChange={(e) =>
          setInstagramUrl(
            e.target.value
          )
        }
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px",
        }}
      />

      <button
        onClick={
          handleInstagramProcess
        }
        disabled={loading}
      >
        {loading
          ? "Processing..."
          : "Process Instagram Reel"}
      </button>
    </div>
  );
}

export default UrlForm;