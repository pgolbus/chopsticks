import React, { useState } from 'react';
import './App.css';

// Define the ASCII art for 0 to 4 fingers
const handStates = [
  `
 O
/|\\
/ \\
  `,
  `
 O
/|\\
 |
/ \\
  `,
  `
 O
/|\\
/|
/ \\
  `,
  `
 O
/|\\
/|\\
/ \\
  `,
  `
 O
/|\\
/|\\
/|\\
  `
];

function App() {
  const [board, setBoard] = useState(Array(9).fill(''));
  const [firstClick, setFirstClick] = useState(null);

  const handleClick = (index) => {
    const newBoard = [...board];

    if (firstClick === null) {
      // First click
      setFirstClick(index);
    } else {
      // Second click
      window.alert(`First Click: ${firstClick}, Second Click: ${index}`);
      setFirstClick(null);
      newBoard[firstClick] = '';
      newBoard[index] = '';
    }

    if ([0, 2, 6, 8].includes(index)) {
      if (newBoard[index] === '') {
        newBoard[index] = handStates[1];
      } else {
        let currentValueIndex = handStates.indexOf(newBoard[index]);
        let newValueIndex = (currentValueIndex + 1) % handStates.length;
        newBoard[index] = handStates[newValueIndex];
      }
    }

    setBoard(newBoard);
  };

  return (
    <div className="App">
      <h1>Tic Tac Toe</h1>
      <div className="board">
        {board.map((cell, index) => (
          <div
            key={index}
            className={`square ${[0, 2, 6, 8].includes(index) ? 'clickable' : ''}`}
            onClick={() => handleClick(index)}
          >
            <pre>{cell}</pre>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
