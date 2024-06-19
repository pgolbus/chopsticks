import React, { useState } from 'react';
import './App.css';
import handStates from './handStates';

function App() {
  const fingers = 5;
  const initialBoard = Array(9).fill('');
  [0, 2, 6, 8].forEach(index => initialBoard[index] = 0);
  const [board, setBoard] = useState(initialBoard);
  // const [firstClick, setFirstClick] = useState(null);

  const handleClick = (index) => {
    const newBoard = [...board];

    /* if (firstClick === null) {
      // First click
      setFirstClick(index);
    } else {
      // Second click
      window.alert(`First Click: ${firstClick}, Second Click: ${index}`);
      setFirstClick(null);
      newBoard[firstClick] = '';
      newBoard[index] = '';
    }*/

    let currentValueIndex = handStates.indexOf(newBoard[index]);
    let newValueIndex = (currentValueIndex + 1) % fingers;
    newBoard[index] = newValueIndex;

    setBoard(newBoard);

  };

  return (
    <div className="App">
      <h1>Chopsticks</h1>
      <div className="board">
        {board.map((cell, index) => (
          <div
            key={index}
            className={`square ${[0, 2, 6, 8].includes(index) ? 'clickable' : ''}`}
            onClick={() => [0, 2, 6, 8].includes(index) && handleClick(index)}
          >
            <pre>{[0, 2, 6, 8].includes(index) ? handStates[cell] : ''}</pre>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
