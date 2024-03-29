import React, { useState, useEffect } from 'react';
import './Dashboard.css'; // Import the CSS file
import electionSymbol from '../Assets/election symbol.png';

const Dashboard = ({ userData, parties, handleVote, handleLogout }) => {
  const [user, setUser] = useState({});
  const [votedParties] = useState([]);

  useEffect(() => {
    // Fetch user data when userData changes (i.e., when login/signup is successful)
    if (userData && userData.voter_Id) {
      fetchUserData(userData.voter_Id);
    }
  }, [userData]);

  useEffect(() => {
    // Refresh user data every 10 seconds
    const interval = setInterval(() => {
      if (user && user.voter_Id) {
        fetchUserData(user.voter_Id);
      }
    }, 10000);

    return () => clearInterval(interval); // Cleanup interval on component unmount
  }, [user]);

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

  const handleLogoutClick = () => {
    handleLogout(); // Call the parent component's handleLogout function
  };

  const handleVoteClick = (party) => {
    if (user && user.status === 'Voted') {
      alert('You have already voted.');
      return;
    }
    handleVote(party);
  };

  return (
    <div className='dashboard-container'>
      <div className='dashboard-header'>
        <h2 className='dashboard-title'><span>Online</span> <span>Voting</span> <span>System</span></h2>
        <button className='logout-button' onClick={handleLogoutClick}>Logout</button>
      </div>
      <div className='image-container'>
        <img src={electionSymbol} alt="Election Symbol" />
      </div>
      <div className='user-info-container'>
        <div className='user-info'>
          {user && user.voter_Id ? (
            <div>
              <h3>User Information:</h3>
              <p>Voter ID: {user.voter_Id}</p>
              <p>Name: {user.name}</p>
              <p>Status: {user.status}</p>
            </div>
          ) : (
            <p>Loading user information...</p>
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
                onClick={() => handleVoteClick(party)}
                disabled={user.status === "Voted" && votedParties.includes(party)}
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
