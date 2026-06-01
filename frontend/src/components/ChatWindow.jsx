import { useState } from "react";
import MessageBubble from "./MessageBubble";
import { streamChat } from "../api";

function ChatWindow() {
  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Ask questions about your uploaded videos.",
    },
  ]);

  const handleSend = async () => {
    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    let botText = "";

    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: "" },
    ]);

    await streamChat(question, (chunk) => {
      botText += chunk;

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "assistant",
          content: botText,
        };
        return updated;
      });
    });

    setQuestion("");
  };

  return (
    <div style={{ width: "800px", marginTop: "30px", border: "1px solid #ddd", borderRadius: "12px" }}>
      
      <div style={{ padding: "15px", backgroundColor: "#111827", color: "white" }}>
        AI Chat Assistant
      </div>

      <div style={{ height: "400px", overflowY: "auto", padding: "20px" }}>
        {messages.map((m, i) => (
          <MessageBubble key={i} role={m.role} content={m.content} />
        ))}
      </div>

      <div style={{ display: "flex", gap: "10px", padding: "15px" }}>
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          style={{ flex: 1, padding: "10px" }}
          placeholder="Ask a question..."
        />

        <button onClick={handleSend}>
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;