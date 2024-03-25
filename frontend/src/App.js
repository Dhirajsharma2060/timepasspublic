import React, { useState } from 'react';
import LoginSignup from './Components/Login/LoginSignup';
import Dashboard from './Components/Login/Dashboard';

const App = () => {
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [voter_Id, setVoterId] = useState(''); // Initialize voter_Id state

  const redirectToDashboard = (voter_Id) => { // Change the parameter name to voterId
    setLoggedIn(true);
    setVoterId(voter_Id); // Set the voterId received from the login/signup component
  };

  // Define the parties array with the names of the four parties
  const parties = ['BJP', 'CONGRESS', 'SHIVSENA', 'AAP'];

  return (
    <div>
      {isLoggedIn ? (
        <Dashboard voter_Id={voter_Id} parties={parties} />
      ) : (
        <LoginSignup onRedirectToDashboard={redirectToDashboard}  /> // Pass voterId to LoginSignup
      )}
    </div>
  );
};

export default App;
