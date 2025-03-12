import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

export default function Welcome() {
    const [username, setUsername] = useState("");
    const navigate = useNavigate();
  
    const handleSubmitUsername = () => {
      if (username.trim()) {
        Cookies.set("username", username, { expires: 7 });
        navigate("/chat"); // Redirect to chatbot
      }
    };
  
    return (
      <div>
        <h1>Welcome! Enter your username:</h1>
        <input
          type="text"
          placeholder="Enter username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <button onClick={handleSubmitUsername}>
          Submit
        </button>
      </div>
    );
  }