import React, { useState, useEffect } from 'react';
import './Dashboard.css'; // Import the CSS file
import electionSymbol from'../Assets/election symbol.png';

const Dashboard = ({ userData, parties, handleVote, votedParty, handleLogout }) => {
  const [user, setUser] = useState({});
  const [votedParties] = useState([]);

  useEffect(() => {
    // Fetch user data when userData changes (i.e., when login/signup is successful)
    if (userData) {
      fetchUserData(userData.voter_Id);
    }
  }, [userData]);

  const fetchUserData = async (voterId) => {
    try {
      if (!voterId) {
        console.error('Voter ID is undefined or null');
        return;
      }

      const response = await fetch(`http://127.0.0.1:8000/dashboard/${encodeURIComponent(voterId)}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error('Failed to fetch user data');
      }
      const data = await response.json();
      console.log('User data:', data); // Log the received data for debugging
      setUser(data);
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  console.log('User state:', user); // Log the user state for debugging

  const handleLogoutClick = () => {
    handleLogout(); // Call the parent component's handleLogout function
  };

  return (
    <div className='dashboard-container'>
      <div className='dashboard-header'>
        <h2 className='dashboard-title'>Online Voting System</h2>
        <button className='logout-button' onClick={handleLogoutClick}>Logout</button>
      </div>
      <div className='image-container'>
        <img src={electionSymbol} alt="Election Symbol" />
      </div>
      <div className='user-info-container'>
        <div className='user-info'>
          {user && (
            <div>
              <h3>User Information:</h3>
              <p>Voter ID: {userData.voter_Id}</p>
              <p>Name: {user.name}</p>
              <p>Status: {user.status}</p>
            </div>
          )}
        </div>
      </div>
      <div className='parties-list-container'>
        <h3>Parties:</h3>
        <ul className='parties-list'>
          {parties.map((party, index) => (
            <li key={index} className='party-item'>
              {party}{' '}
              <button
                onClick={() => handleVote(party)}
                disabled={user.status === "voted" && votedParties.includes(party)}
                className='vote-button'
              >
                Vote
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;