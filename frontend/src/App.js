import React, { useState, useEffect } from 'react';
import LoginSignup from './Components/Login/LoginSignup';
import Dashboard from './Components/Login/Dashboard';

const App = () => {
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);
  const [votedParty, setVotedParty] = useState(null);

  const redirectToDashboard = async (responseData) => {
    setLoggedIn(true);
    setUserData(responseData); // Make sure responseData includes 'status'
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
      
      const responseData = await response.json();
      setVotedParty(party);
      setUserData(responseData); // Update after successful vote
    } catch (error) {
      console.error('Error voting:', error);
    }
  };

  const handleLogout = () => {
    setLoggedIn(false);
    setUserData(null);
  };

  const parties = ['BJP', 'CONGRESS', 'SHIVSENA', 'AAP', 'NOTA'];

  // Check user status on initial render and after login
  // ... previous code ...

  useEffect(() => {
    const checkUserStatus = async () => {
      if (userData && userData.voter_Id) {
        // If `userData.status` is available and reliable, use it directly:
        if (userData.status !== "Voted") {
          console.log(userData.status); // Log the status for reference
          // Display alert or notification based on status (using library or custom component)
          if (userData.status === "Voted") {
            console.log("User has already voted");
            // ... Display alert (consider using a notification library)
          } else {
            console.log("User has not voted yet");
          }
        } else {
          // If `userData.status` is not reliable or not available:
          try {
            // Fetch status from the API endpoint:
            const response = await fetch(`http://127.0.0.1:8000/dashboard/${userData.voter_Id}`); // Assuming the endpoint returns status
            const responseData = await response.json();
            if (responseData.status === "Voted") {
              console.log("User has already voted (fetched from API)");
              // ... Display alert (consider using a notification library)
            } else {
              console.log("User has not voted yet (fetched from API)");
            }
          } catch (error) {
            console.error("Error fetching status:", error);
            // Handle API error gracefully (e.g., retry or display error message)
          }
        }
      }
    };
  
    checkUserStatus();
  }, [userData]);
  

// ... rest of the code ...

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
