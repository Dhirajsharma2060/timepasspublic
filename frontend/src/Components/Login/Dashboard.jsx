import React, { useState } from 'react';

const Dashboard = ({ voterId, parties }) => {
  const [votedParties, setVotedParties] = useState([]);

  const handleVote = (party) => {
    if (votedParties.includes(party)) {
      alert(`You have already voted for ${party}`);
    } else {
      setVotedParties([...votedParties, party]);
      console.log(`Voted for ${party}`);
    }
  };

  return (
    <div className='dashboard-container' style={{ backgroundColor: 'cyan', minHeight: '100vh', padding: '20px' }}>
      <h2>Welcome, Voter {voterId}</h2>
      <h3>Parties:</h3>
      <ul>
        {parties.map((party, index) => (
          <li key={index} style={{ marginBottom: '10px' }}>
            {party}{' '}
            <button
              onClick={() => handleVote(party)}
              style={{ marginLeft: '10px', padding: '5px 10px', borderRadius: '5px', backgroundColor: '#007bff', color: 'white', border: 'none', cursor: 'pointer' }}
            >
              Vote
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
