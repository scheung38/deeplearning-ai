import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

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

  return (
    <>
      <div>
        <a href="[https://vite.dev](https://vite.dev)" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="[https://react.dev](https://react.dev)" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Wikipedia Category Word Cloud</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          placeholder="Enter category"
        />
        <button type="submit">Generate Word Cloud</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <div>
        <h2>Word Cloud</h2>
        
        <ul>
          {Object.entries(wordFrequencies).map(([word, count]) =>
            typeof count === "number" ? (
              <li key={word} style={{ fontSize: `${count}px` }}>
                {word}: {count}
              </li>
            ) : (
              <li key={word} style={{ fontSize: `${count}px` }}>
                {word}: null
              </li>
            )
          )}
        </ul>
      </div>
    </>
  );
}

export default App;
