import UrlForm from "./components/UrlForm";
import ChatWindow from "./components/ChatWindow";

function App() {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "30px",
      }}
    >
      <h1>Social Media RAG Assistant</h1>

      <UrlForm />

      <ChatWindow />
    </div>
  );
}

export default App;