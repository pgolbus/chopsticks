import React, { useCallback, useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import handStates from './handStates';

const URL = 'http://172.21.113.211:5000/chopsticks';

const App = () => {
  const initialBoard = Array(9).fill('');
  const player1cells = [0, 6];
  const player2cells = [2, 8];
  const hands = {
    0: "left",
    2: "left",
    6: "right",
    8: "right"
  };
  const playerCells = [...player1cells, ...player2cells];
  const player1TextCell = 3;
  const player1Text = "Player 1";
  const player2TextCell = 5;
  const player2Text = "Player 2";
  const [board, setBoard] = useState(initialBoard);
  const [firstClick, setFirstClick] = useState(null);
  const [playerTurn, setPlayerTurn] = useState(0);

  const updateBoard = useCallback(() => {
    console.log("updateBoard called");
    axios.get(`${URL}/get_board_state`)
      .then(response => {
        console.log("Board state response:", response.data);
        let boardUpdate = response.data;
        let newBoard = Array(9).fill('');
        newBoard[0] = boardUpdate.player1_left;
        newBoard[2] = boardUpdate.player2_left;
        newBoard[6] = boardUpdate.player1_right;
        newBoard[8] = boardUpdate.player2_right;
        console.log("New board state before setBoard:", newBoard);
        setBoard(newBoard);
      })
      .catch(error => {
        console.error('Error fetching board state:', error);
      });
  }, []);

  useEffect(() => {
    updateBoard(); // Fetch initial board state on mount
  }, [updateBoard]); // Dependency array with updateBoard

  useEffect(() => {
    console.log("Board state changed:", board);
  }, [board]);

  const renderCell = (cell, index) => {
    if (playerCells.includes(index)) {
      return handStates[cell];
    } else if (index === player1TextCell) {
      return player1Text;
    } else if (index === player2TextCell) {
      return player2Text;
    }
  };

  const updatePlayer = () => {
    axios.get(`${URL}/get_current_player`)
      .then(response => {
        setPlayerTurn(response.data.player);
      })
      .catch(error => {
        console.error('Error fetching current player:', error);
      });
  };

  const firstClickSetter = (index, player, hand) => {
    axios.get(`${URL}/get_player_hand/${player}/${hand}`)
      .then(response => {
        console.log("Player hand response:", response.data);
        let fingers = response.data.hand;
        if (fingers === 0) {
          window.alert('Cannot add fingers to an empty hand');
          throw new Error('Cannot add fingers to an empty hand');
        }
        setFirstClick(index);
      })
      .catch(error => {
        if (error.message !== 'Cannot add fingers to an empty hand') {
          console.error('Error fetching data:', error);
        }
      });
  };

  const handleClick = (index) => {
    console.log("handleClick called with index:", index);
    if (firstClick === null) {
      updatePlayer()
      if (
            (playerTurn === 0 && !player1cells.includes(index)) ||
            (playerTurn === 1 && !player2cells.includes(index))
          )
      {
        window.alert('You must start with one of your own hands');
        throw new Error('Invalid starting hand');
      }
      firstClickSetter(index, playerTurn, hands[index]);
    } else {
      if (index === firstClick) {
        window.alert('You must pick a different hand');
        return;
      }
      if ((player1cells.includes(firstClick) && player1cells.includes(index)) ||
          (player2cells.includes(firstClick) && player2cells.includes(index))) {
        let toSwap = window.prompt('How many would you like to swap?');
        axios.get(`${URL}/swap/${playerTurn}/${hands[firstClick]}/${toSwap}`)
        .then(response => {
          console.log("Swap response:", response.data);
          updatePlayer();
          updateBoard();
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
      } else {
        axios.get(`${URL}/move/${playerTurn}/${hands[firstClick]}/${hands[index]}`)
          .then(response => {
            console.log("Move response:", response.data);
            updatePlayer();
            updateBoard();
          })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
      }
    }
  }

  const handleReset = () => {
    axios.get(`${URL}/chopsticks/reset`)
      .then(response => {
        console.log('Game reset successfully:', response.data);
        updatePlayer();
        updateBoard();
      })
      .catch(error => {
        console.error('Failed to reset game:', error);
      });
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
      <button
        className="reset-button"
        onClick={handleReset}
      >
        Reset
      </button>
    </div>
  );
};

export default App;
