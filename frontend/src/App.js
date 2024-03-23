import React, { useState } from 'react';
import LoginSignup from './Components/Login/LoginSignup';
import Dashboard from './Components/Login/Dashboard';

const App = () => {
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [voterId, setVoterId] = useState('');

  const redirectToDashboard = (id) => {
    setLoggedIn(true);
    setVoterId(id);
  };

  // Define the parties array with the names of the four parties
  const parties = ['BJP', 'CONGRESS', 'SHIVSENA', 'AAP'];

  return (
    <div>
      {isLoggedIn ? (
        <Dashboard voterId={voterId} parties={parties} />
      ) : (
        <LoginSignup onRedirectToDashboard={redirectToDashboard} />
      )}
    </div>
  );
};

export default App;

