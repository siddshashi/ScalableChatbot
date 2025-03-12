import React, { useEffect, useState } from 'react';
import api from "../api.js";
import AddQueryForm from './AddQueryForm.jsx';
import { useUsername } from "../hooks/useUsername";


const QueryList = () => {
  const username = useUsername(); 
  const [queries, setQueries] = useState([]);

  const fetchQueries = async () => {
    try {
      const response = await api.get('/queries', 
      {
        headers: { "Username": username }
      }
    );
      setQueries(response.data.queries);
    } catch (error) {
      console.error("Error fetching queries", error);
    }
  };

  const addQuery = async (question) => {
    try {
      await api.post('/queries', { question: question },
        {
          headers: {"Username": username }  
        }
      );
      fetchQueries();  // Refresh the list after adding a query
    } catch (error) {
      console.error("Error adding query", error);
    }
  };

  useEffect(() => { // for some reason, this is not running at startup for a second concurrent user with the same name
    fetchQueries();
  }, []);

  return (
    <div>
      <h2>Query List</h2>
      <ul>
        {queries.map((query, index) => (
          <li key={index}>
            {query.question}
            <br />
            {query.response}
            </li>
        ))}
      </ul>
      <AddQueryForm addQuery={addQuery} />
    </div>
  );
};

export default QueryList;