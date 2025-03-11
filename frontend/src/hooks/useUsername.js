import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

export function useUsername() {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const storedUsername = Cookies.get("username");
    if (!storedUsername) {
      navigate("/"); // Redirect to Welcome if no username
    } else {
      setUsername(storedUsername);
    }
  }, [navigate]);

  return username;
}