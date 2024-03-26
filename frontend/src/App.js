import React, { useState } from 'react';
import LoginSignup from './Components/Login/LoginSignup';
import Dashboard from './Components/Login/Dashboard';

const App = () => {
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null); // Initialize userData state

  const redirectToDashboard = async (responseData) => {
    setLoggedIn(true);
    setUserData(responseData); // Set the response data received from login/signup
  };

  // Define the parties array with the names of the four parties
  const parties = ['BJP', 'CONGRESS', 'SHIVSENA', 'AAP'];

  return (
    <div>
      {isLoggedIn ? (
        <Dashboard userData={userData} parties={parties} />
      ) : (
        <LoginSignup onRedirectToDashboard={redirectToDashboard} />
      )}
    </div>
  );
};

export default App;
