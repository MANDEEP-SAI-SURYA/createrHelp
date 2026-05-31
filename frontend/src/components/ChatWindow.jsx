import { useState } from "react";
import MessageBubble from "./MessageBubble";

function ChatWindow() {
  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! Upload your YouTube and Instagram URLs, then ask me questions about the videos.",
    },
  ]);

  const handleSend = () => {
    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      content: question,
    };

    const assistantMessage = {
      role: "assistant",
      content:
        "This is a placeholder response. Later we will connect FastAPI + Groq here.",
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
      assistantMessage,
    ]);

    setQuestion("");
  };

  return (
    <div
      style={{
        width: "800px",
        marginTop: "30px",
        border: "1px solid #ddd",
        borderRadius: "12px",
        overflow: "hidden",
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: "15px",
          backgroundColor: "#111827",
          color: "white",
          fontWeight: "bold",
        }}
      >
        AI Chat Assistant
      </div>

      {/* Messages */}
      <div
        style={{
          height: "400px",
          overflowY: "auto",
          padding: "20px",
          backgroundColor: "#f9fafb",
        }}
      >
        {messages.map((message, index) => (
          <MessageBubble
            key={index}
            role={message.role}
            content={message.content}
          />
        ))}
      </div>

      {/* Input Area */}
      <div
        style={{
          display: "flex",
          gap: "10px",
          padding: "15px",
          borderTop: "1px solid #ddd",
        }}
      >
        <input
          type="text"
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSend();
            }
          }}
          style={{
            flex: 1,
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #ccc",
          }}
        />

        <button
          onClick={handleSend}
          style={{
            padding: "12px 20px",
            backgroundColor: "#2563eb",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;