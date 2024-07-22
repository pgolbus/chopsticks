import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [currentPlayer, setCurrentPlayer] = useState(null);
  const [moveResult, setMoveResult] = useState(null);

  useEffect(() => {
    axios.get('http://172.18.4.181:5000/chopsticks/get_current_player')
      .then(playerResponse => {
        const player = playerResponse.data.player;
        setCurrentPlayer(player);

        return axios.get(`http://172.18.4.181:5000/chopsticks/move/${player}/left/left`);
      })
      .then(moveResponse => {
        setMoveResult(moveResponse.data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div>
      <h1>Current Player: {currentPlayer !== null ? currentPlayer : 'Loading...'}</h1>
      <div>
        <h2>Move Result:</h2>
        <pre>{moveResult !== null ? JSON.stringify(moveResult, null, 2) : 'Loading move result...'}</pre>
      </div>
    </div>
  );
};

export default App;
