import React, { useState } from 'react';
import './App.css';
import handStates from './handStates';

function App() {
  const fingers = 5;
  const initialBoard = Array(9).fill('');
  const player1 = [0, 6];
  const player2 = [2, 8];
  const playerCells = [0, 2, 6, 8];
  const player1TextCell = 3;
  const player2TextCell = 5;
  playerCells.forEach(index => initialBoard[index] = 1);
  const [board, setBoard] = useState(initialBoard);
  const [firstClick, setFirstClick] = useState(null);
  const [playerTurn, setPlayerTurn] = useState(0);

  const flip = () => {
    setPlayerTurn(playerTurn === 0 ? 1 : 0);
  };

  const renderCell = (cell, index) => {
    if (playerCells.includes(index)) {
      return handStates[cell];
    } else if (index === player1TextCell) {
      return 'Player 1';
    } else if (index === player2TextCell) {
      return 'Player 2';
    }
  };

  const handleClick = (index) => {
    console.log(board);
    const newBoard = [...board];

    if (firstClick === null) {
      // First click
      if (newBoard[index] === 0) {
        window.alert('Cannot start with a hand with no fingers');
        return;
      } else if ( 
        (playerTurn === 0 && !player1.includes(index)) || 
        (playerTurn === 1 && !player2.includes(index))
      ) {
        window.alert('You must start with one of your own hands');
        return;
      }
      setFirstClick(index);
    } else {
      // Second click
      if (index === firstClick) {
        window.alert('You must pick a different hand');
        return;
      } else if (
        (playerTurn === 0 && player1.includes(index)) || 
        (playerTurn === 1 && player2.includes(index))
      ) {
        window.alert('I haven\'t built that yet');
        return;
      }
      // window.alert(`First Click: ${firstClick}, Second Click: ${index}`);
      /* let current = newBoard[index];
      let newValue = (current + 1) % fingers;
      newBoard[index] = newValue; */

      let current = newBoard[firstClick];
      let newValue = (current + newBoard[index]) % fingers;
      newBoard[index] = newValue;

      setFirstClick(null);
      flip();
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
            className={`square ${playerCells.includes(index) ? 'clickable' : ''}`}
            onClick={() => playerCells.includes(index) && handleClick(index)}
          >
            <pre>{renderCell(cell, index)}</pre>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
