import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import handStates from './handStates';

const URL = 'http://172.21.113.211:5000/chopsticks';

const App = () => {
  const fingers = 5;
  const initialBoard = Array(9).fill('');
  const player1cells = [0, 6];
  const player2cells = [2, 8];
  const hands = {
    0: "left",
    2: "left",
    6: "right",
    8: "right"
  }
  const playerCells = [...player1cells, ...player2cells];
  const player1TextCell = 3;
  const player1Text = "Player 1";
  const player2TextCell = 5;
  const player2Text = "Player 2";
  playerCells.forEach(index => initialBoard[index] = 1);
  const [board, setBoard] = useState(initialBoard);
  const [firstClick, setFirstClick] = useState(null);
  const [currentPlayer, setCurrentPlayer] = useState(null);
  const [moveResult, setMoveResult] = useState(null);
  const [playerTurn, setPlayerTurn] = useState(0);

  const renderCell = (cell, index) => {
    if (playerCells.includes(index)) {
      return handStates[cell];
    } else if (index === player1TextCell) {
      return player1Text;
    } else if (index === player2TextCell) {
      return player2Text;
    }
  };

  const updateBoard = (boardUpdate) => {
    let newBoard = [...board];
    newBoard[0] = boardUpdate.player1left;
    newBoard[2] = boardUpdate.player2left;
    newBoard[6] = boardUpdate.player1right;
    newBoard[8] = boardUpdate.player2right;
    setBoard(newBoard);
  };

  const handleClick = (index) => {
    if (firstClick === null) {
      axios.get(`${URL}/get_current_player`)
        .then(response => {
          let playerTurn = response.data.player;
          if (
               (playerTurn === 0 && !player1cells.includes(index)) ||
               (playerTurn === 1 && !player2cells.includes(index))
             )
          {
            window.alert('You must start with one of your own hands');
            throw new Error('Invalid starting hand');
          }
          setPlayerTurn(playerTurn);
        }).then(() => {
          if (player1cells.includes(index)) {
            return axios.get(`${URL}/get_player_hand/0/${hands[index]}`)
          }
          return axios.get(`${URL}/get_player_hand/1/${hands[index]}`)
        }).then(response => {
            let fingers = response.data.hand;
            if (fingers === 0) {
              window.alert('Cannot add fingers to an empty hand');
              throw new Error('Cannot add fingers to an empty hand');
            }

          setFirstClick(index);
        })
        .catch(error => {
          if (error.message !== 'Invalid starting hand' && error.message !== 'Cannot add fingers to an empty hand') {
            console.error('Error fetching data:', error);
          }
        });
    } else {
      if (index === firstClick) {
        window.alert('You must pick a different hand');
        return;
      }
      if ((player1cells.includes(firstClick) && player1cells.includes(index) ||
          (player2cells.includes(firstClick) && player2cells.includes(index)))) {
        let toSwap = window.prompt('How many would you like to swap?');
        axios.get(`${URL}/swap/${currentPlayer}/${hands[firstClick]}/${toSwap}`)
        .then(response => {
          updateBoard(response.data);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
      }
    }
  }

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
