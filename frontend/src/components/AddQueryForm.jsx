import React, { useState } from 'react';

const AddQueryForm = ({ addQuery }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (query) {
      addQuery(query);
      setQuery('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter Question"
      />
      <button type="submit">Submit</button>
    </form>
  );
};

export default AddQueryForm;