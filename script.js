// Replace 'voter_id' with the actual voter ID you want to fetch information for
const voterId = 'voter_id';
const url = `http://localhost:8000/dashboard/${voterId}`;

fetch(url)
    .then(response => response.json())
    .then(data => {
        const voterInfoDiv = document.getElementById('voter-info');
        voterInfoDiv.innerHTML = `
            <h2>${data.user.name}</h2>
            <p>Voter ID: ${data.user.voter_id}</p>
            <p>Status: ${data.user.status}</p>
        `;

        // Conditionally render the voting button if the status is 'Not Voted'
        if (data.user.status === 'Not Voted') {
            const voteButton = document.createElement('button');
            voteButton.textContent = 'Vote';
            voteButton.onclick = () => {
                // Implement voting functionality here
                console.log('Voting...');
            };
            voterInfoDiv.appendChild(voteButton);
        }
    })
    .catch(error => console.error('Error fetching voter information:', error));
