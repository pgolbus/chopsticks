import React, { useCallback, useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import handStates from './handStates';  // Importing hand state configurations

const URL = process.env.REACT_APP_FLASK_API;
console.log("apiUrl: ", URL);

axios.get(`${URL}/healthcheck`)
  .then(response => {
    console.log('Health check response:', response.data);
  })
  .catch(error => {
    console.error('Health check failed:', error);
  });

const App = () => {
  // State initialization for the game board
  // This could all be better...
  const initialBoard = Array(9).fill('');
  const player1cells = [0, 6];  // Cells controlled by Player 1
  const player2cells = [2, 8];  // Cells controlled by Player 2
  const hands = {  // Mapping of cell indexes to hand names
    0: "left",
    2: "left",
    6: "right",
    8: "right"
  };
  const playerCells = [...player1cells, ...player2cells];  // Combined cells for easier reference
  const player1TextCell = 3;
  const player1Text = "Player 1";
  const player2TextCell = 5;
  const player2Text = "Player 2";
  const [board, setBoard] = useState(initialBoard);
  const [firstClick, setFirstClick] = useState(null);
  const [playerTurn, setPlayerTurn] = useState(0);

  // Function to reset the game state
  const handleReset = useCallback(() => {
    axios.get(`${URL}/reset`)
      .then(response => {
        console.log('Game reset successfully:', response.data);
        updatePlayer();
        updateBoard();
      })
      .catch(error => {
        console.error('Failed to reset game:', error);
      });
  }, [URL]);

  // Function to fetch and update the board state from the backend
  const updateBoard = useCallback(() => {
    console.log("updateBoard called");
    axios.get(`${URL}/get_board_state`)
      .then(response => {
        console.log("Board state response:", response.data);
        let boardUpdate = response.data;
        if (boardUpdate.winner !== -1) {
          window.alert(`Player ${boardUpdate.winner + 1} wins!`, handleReset());
        }
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
  }, [URL, handleReset]);

  // Effect to initialize the board on component mount
  useEffect(() => {
    updateBoard();
  }, [updateBoard]);

  // Effect to log changes in the board state
  useEffect(() => {
    console.log("Board state changed:", board);
  }, [board]);

  // Function to render cells based on their type and state
  const renderCell = (cell, index) => {
    if (playerCells.includes(index)) {
      return handStates[cell];
    } else if (index === player1TextCell) {
      return player1Text;
    } else if (index === player2TextCell) {
      return player2Text;
    }
  };

  // Function to fetch the current player's turn from the backend
  const updatePlayer = useCallback(() => {
    axios.get(`${URL}/get_current_player`)
      .then(response => {
        setPlayerTurn(response.data.player);
      })
      .catch(error => {
        console.error('Error fetching current player:', error);
      });
  }, [URL]);

  // Function to handle the first click in a game move
  const firstClickSetter = useCallback((index, player, hand) => {
    const firstClickUrl = `${URL}/get_player_hand/${player}/${hand}`;
    console.log("firstClickUrl:", firstClickUrl);
    axios.get(firstClickUrl)
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
  }, [URL]);

  // Function to handle subsequent clicks and perform game actions like move or swap
  const handleClick = useCallback((index) => {
    console.log("handleClick called with index:", index);
    if (firstClick === null) {
      updatePlayer();
      if ((playerTurn === 0 && !player1cells.includes(index)) ||
          (playerTurn === 1 && !player2cells.includes(index))) {
        window.alert('You must start with one of your own hands');
        throw new Error('Invalid starting hand');
      }
      firstClickSetter(index, playerTurn, hands[index]);
    } else {
      if (index === firstClick) {
        window.alert('You must pick a different hand');
        return;
      }
      console.log("firstClick:", firstClick, "index:", index);
      if ((player1cells.includes(firstClick) && player1cells.includes(index)) ||
          (player2cells.includes(firstClick) && player2cells.includes(index))) {
        let toSwap = window.prompt('How many would you like to swap?');
        const swapUrl = `${URL}/swap/${playerTurn}/${hands[firstClick]}/${toSwap}`;
        console.log("swapUrl:", swapUrl);
        axios.get(swapUrl)
        .then(response => {
          console.log("Swap response:", response.data);
          updatePlayer();
          updateBoard();
        })
        .catch(error => {
          // Handle error response
          if (error.response && error.response.data && error.response.data.error) {
            if (error.response.data.error === 'Cannot swap all / more fingers than you have.') {
              console.error('Cannot swap all / more fingers than you have.', error.response.data.error);
              window.alert('Cannot swap all / more fingers than you have. Try again.');
              setFirstClick(null);
            } else {
              console.error('Other error occurred:', error.response.data.error);
              // Handle other errors
            }
          }
        });
      } else {
        const moveUrl = `${URL}/move/${playerTurn}/${hands[firstClick]}/${hands[index]}`;
        console.log("moveUrl:", moveUrl);
        axios.get(moveUrl)
          .then(response => {
            console.log("Move response:", response.data);
            updatePlayer();
            updateBoard();
          })
          .catch(error => {
            // Handle error response
            if (error.response && error.response.data && error.response.data.error) {
              if (error.response.data.error === 'Cannot move from / to an empty hand.') {
                console.error('Cannot move from / to an empty hand.:', error.response.data.error);
                window.alert('Cannot move from / to an empty hand.  Try again.');
                setFirstClick(null);
              } else {
                console.error('Other error occurred:', error.response.data.error);
                // Handle other errors
              }
            } else {
              console.error('Error fetching data:', error);
            }
          })
      }
      setFirstClick(null);
    }
  }, [firstClick, playerTurn, player1cells, player2cells, hands, URL, updatePlayer, updateBoard]);

  // Main component render method
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