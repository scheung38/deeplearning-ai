import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import WordCloud from "react-d3-cloud";

function App() {
  const [wordFrequencies, setWordFrequencies] = useState({});
  const [category, setCategory] = useState("");
  const [error, setError] = useState("");

  const fetchWordFrequencies = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/word-frequencies/${category}`
      );
      if (!response.ok) {
        throw new Error("No data found for the given category");
      }
      const data = await response.json();
      setWordFrequencies(data);
      setError("");
    } catch (error) {
      setError((error as Error).message);
    }
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    fetchWordFrequencies();
  };

  const words = Object.entries(wordFrequencies).map(([word, count]) => ({
    text: word,
    value: typeof count === "number" ? count : 0,
  }));

  return (
    <>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "100vh",
        }}
      >
        <a href="[https://vite.dev](https://vite.dev)" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="[https://react.dev](https://react.dev)" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1 style={{ textAlign: "center" }}>Wikipedia Category Word Cloud</h1>
      <form
        onSubmit={handleSubmit}
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "10px",
          margin: "20px 0",
        }}
      >
        <input
          type="text"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          placeholder="Enter category"
          style={{ height: "40px", color: "white" }}
        />
        <button
          type="submit"
          style={{ backgroundColor: "green", color: "white", height: "40px" }}
        >
          Generate Word Cloud
        </button>
      </form>
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
      <div>
        <h2 style={{ textAlign: "center" }}>Word Cloud</h2>
        <div style={{ backgroundColor: "#f5f5dc" }}>
          <WordCloud
            data={words}
            // fontSizeMapper={(word) => Math.log2(word.value) * 5}
            // rotate={() => 0}
          />
        </div>
      </div>
    </>
  );
}

export default App;
