import React, { useState } from 'react';
import './App.css';
import handStates from './handStates';

function App() {
  const fingers = 5;
  const initialBoard = Array(9).fill('');
  [0, 2, 6, 8].forEach(index => initialBoard[index] = 1);
  const [board, setBoard] = useState(initialBoard);
  const [firstClick, setFirstClick] = useState(null);
  const [playerTurn, setPlayerTurn] = useState(0);

  const flip = (turn) => {
    setPlayerTurn(turn === 0 ? 1 : 0);
  };

  const handleClick = (index) => {
    console.log(board);
    const newBoard = [...board];

    if (firstClick === null) {
      // First click
      if (newBoard[index] === 0) {
        window.alert('Cannot start with a hand with no fingers');
        return;
      }
      setFirstClick(index);
    } else {
      // Second click
      if (index === firstClick) {
        window.alert('You must pick a different hand');
        return;
      }
      // window.alert(`First Click: ${firstClick}, Second Click: ${index}`);

      let current = newBoard[firstClick];
      let newValue = (current + newBoard[index]) % fingers;
      newBoard[index] = newValue;

      setFirstClick(null);

      /* let current = newBoard[index];
      let newValue = (current + 1) % fingers;
      newBoard[index] = newValue; */

      setBoard(newBoard);
    }
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
