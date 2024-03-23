// apiService.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000'; // Replace with your FastAPI backend URL

// Function to register a new user
export const registerUser = async (voterId, username, password) => {
  try {
    const response = await axios.post(`${API_URL}/register`, {
      voter_Id: voterId,
      username: username,
      password: password,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response.data.detail);
  }
};

// Function to login a user
export const loginUser = async (voterId, password) => {
  try {
    const response = await axios.post(`${API_URL}/login`, {
      voter_Id: voterId,
      password: password,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response.data.detail);
  }
};

// Other API functions can be added as needed
