import QueryList  from "../components/Queries";
import { useUsername } from "../hooks/useUsername";

export default function Chat() {
  const username = useUsername(); 

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
