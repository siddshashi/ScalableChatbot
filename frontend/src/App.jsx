import React from 'react';
import './App.css';
import QueryList from './components/Queries';

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Scalable Chatbot</h1>
      </header>
      <main>
        <QueryList />
      </main>
    </div>
  );
};

export default App;