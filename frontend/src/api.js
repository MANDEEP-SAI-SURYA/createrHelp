const BASE_URL = "http://127.0.0.1:8000";

// Upload YouTube URL
export const processYoutube = async (url) => {
  const res = await fetch(`${BASE_URL}/youtube`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url }),
  });

  return res.json();
};

// Streaming chat
export const streamChat = async (question, onChunk) => {
  const res = await fetch(`${BASE_URL}/chat-stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  const reader = res.body.getReader();
  const decoder = new TextDecoder("utf-8");

  let fullText = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    fullText += chunk;

    onChunk(chunk);
  }

  return fullText;
};


export const processInstagram = async (url) => {
  const response = await fetch(
    "http://127.0.0.1:8000/instagram",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(
      "Instagram processing failed"
    );
  }

  return response.json();
};