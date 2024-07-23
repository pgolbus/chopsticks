import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import handStates from './handStates';

function App() {
  const fingers = 5;
  const initialBoard = Array(9).fill('');
  const player1cells = [0, 6];
  const player2cells = [2, 8];
  const playerCells = [...player1cells, ...player2cells];
  const player1TextCell = 3;
  const player1Text = "Player 1";
  const player2TextCell = 5;
  const player2Text = "Player 2";
  playerCells.forEach(index => initialBoard[index] = 1);
  const [board, setBoard] = useState(initialBoard);
  const [firstClick, setFirstClick] = useState(null);
  const [playerTurn, setPlayerTurn] = useState(0);

   // Change between player 1 and player 2
  const getCurrentPlayer = async () => {
    try {
      const response = await axios.get('http://172.18.4.181:5000/chopsticks/get_current_player');
      console.log(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  getCurrentPlayer()

  const win = (newBoard) => {
    console.log(newBoard);
    if (playerTurn === 0) {
      return player2cells.every(index => newBoard[index] === 0);
    }
    if (playerTurn === 1) {
      return player1cells.every(index => newBoard[index] === 0);
    }
    return false;
  };

  // Swap fingers between hands
  const swap = (index, board) => {
    const newBoard = [...board];
    while (true) {
      let toSwap = window.prompt('How many would you like to swap?');
      // if it's not an integer, continue
      if (!Number.isInteger(Number(toSwap))) {
        window.alert('Please enter an integer');
        continue;
      }
      toSwap = Number(toSwap);
      // if it's not between 1 and newBoard[firstClick] -1, continue
      if (toSwap < 1 || toSwap > newBoard[firstClick] - 1) {
        window.alert(`Please enter a number between 1 and ${newBoard[firstClick] - 1}`);
        continue;
      } else {
        newBoard[firstClick] -= toSwap;
        let current = newBoard[index];
        newBoard[index] = (current + toSwap) % fingers;
        return newBoard;
      }
    }
  };

  const renderCell = (cell, index) => {
    if (playerCells.includes(index)) {
      return handStates[cell];
    } else if (index === player1TextCell) {
      return player1Text;
    } else if (index === player2TextCell) {
      return player2Text;
    }
  };

  const handleClick = (index) => {
    let newBoard = [...board];

    if (firstClick === null) {
      // First click
      if (newBoard[index] === 0) {
        window.alert('Cannot start with a hand with no fingers');
        return;
      } else if (
        (playerTurn === 0 && !player1cells.includes(index)) ||
        (playerTurn === 1 && !player2cells.includes(index))
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
      } else if (newBoard[index] === 0) {
        window.alert('Cannot add fingers to an empty hand');
        return;
      } else if (
        (playerTurn === 0 && player1cells.includes(index)) ||
        (playerTurn === 1 && player2cells.includes(index))
      ) {
        if (newBoard[firstClick] === 1) {
          window.alert('You must pick a hand with at least two fingers to swap from');
          setFirstClick(null);
          return;
        }
        newBoard = swap(index, newBoard);
      } else {
        // window.alert(`First Click: ${firstClick}, Second Click: ${index}`);
        let current = newBoard[index];
        let newValue = (current + 1) % fingers;
        newBoard[index] = newValue;

        let current = newBoard[firstClick];
        let newValue = (current + newBoard[index]) % fingers;
        newBoard[index] = newValue;
      }

      setFirstClick(null);
      setBoard(newBoard);
      if (win(newBoard)) {
        window.alert(`Player ${playerTurn + 1} wins!`);
        return;
      }
      flip();
    }
  };

  return (
    <div className="App">
      <h1>Chopsticks</h1>
      <div className="board">
        {board.map((cell, index) => (
          <div
            key={index}
            className={`square ${playerCells.includes(index) ? 'clickable' : ''}
              ${index === player1TextCell && playerTurn === 0 ? 'active-player' : ''}
              ${index === player2TextCell && playerTurn === 1 ? 'active-player' : ''}`}
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
