import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";
import QueryList  from "../components/Queries";

export default function Chat() {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const storedUsername = Cookies.get("username");
    if (!storedUsername) {
      navigate("/"); // Redirect if no username
    } else {
      setUsername(storedUsername);
    }
  }, [navigate]);

  return (
    <div>
      <h1>Hello, {username}!</h1>
      <h1>Scalable Chatbot</h1>
      <main>
        <QueryList />
      </main>
    </div>
  );
}
