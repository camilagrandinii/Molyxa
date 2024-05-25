import './App.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [elements, setElements] = useState([]);
  const [moodBoard, setMoodBoard] = useState([]);

  useEffect(() => {
    // Fetch elements from the backend
    axios.get('/api/elements')
      .then(response => {
        setElements(response.data);
      });
    // Fetch mood board elements from the backend
    axios.get('/api/mood-board')
      .then(response => {
        setMoodBoard(response.data);
      });
  }, []);

  const addToMoodBoard = (element) => {
    axios.post('/api/mood-board', element)
      .then(response => {
        setMoodBoard(response.data);
      });
  };

  const removeFromMoodBoard = (id) => {
    axios.delete(`/api/mood-board/${id}`)
      .then(response => {
        setMoodBoard(response.data);
      });
  };

  return (
    <div className="App">
      <h1>Mood Board</h1>
      <div className="elements">
        <h2>Elements</h2>
        {elements.map(element => (
          <div key={element.id} className="element" onClick={() => addToMoodBoard(element)}>
            {element.type === 'image' ? <img src={element.src} alt=""/> : <p>{element.text}</p>}
          </div>
        ))}
      </div>
      <div className="mood-board">
        <h2>Your Mood Board</h2>
        {moodBoard.map(item => (
          <div key={item.id} className="mood-board-item" onClick={() => removeFromMoodBoard(item.id)}>
            {item.type === 'image' ? <img src={item.src} alt=""/> : <p>{item.text}</p>}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;

