import React, { useState } from 'react';
import LoginSignup from './Components/Login/LoginSignup';
import Dashboard from './Components/Login/Dashboard';

const App = () => {
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null); // Initialize userData state
  const [votedParty, setVotedParty] = useState(null);

  const redirectToDashboard = async (responseData) => {
    setLoggedIn(true);
    setUserData(responseData); // Set the response data received from login/signup
  };
  const handleVote = async (party) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/vote/${encodeURIComponent(userData.voter_Id)}/${encodeURIComponent(party)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error('Failed to vote');
      }

      setVotedParty(party);
      // Debugging: Log the value of userData.status
      console.log('User status:', userData.status);

      // Check if the user's status is "voted" before showing the alert
      if (userData.status === "Voted") {
        console.log("User has already voted");
        alert("You have already voted. You cannot vote more than once.");
      } else {
        console.log("User has not voted yet");
        alert(`Vote for ${party} recorded successfully`);
      }
    } catch (error) {
      console.error('Error voting:', error);
    }
  };  
  const handleLogout = () => {
    setLoggedIn(false); // Set isLoggedIn state to false
    setUserData(null); // Clear userData state
  };

  // Define the parties array with the names of the four parties
  const parties = ['BJP', 'CONGRESS', 'SHIVSENA', 'AAP','NOTA'];

  return (
    <div>
      {isLoggedIn ? (
        <Dashboard userData={userData} parties={parties} handleVote={handleVote} votedParty={votedParty} handleLogout={handleLogout} />
      ) : (
        <LoginSignup onRedirectToDashboard={redirectToDashboard} />
      )}
    </div>
  );
};

export default App;