import React, { useState } from 'react';
import './LoginSignup.css';
import userIcon from '../Assets/person.png';
import pancardIcon from '../Assets/email.png';
import passwordIcon from '../Assets/password.png';

const LoginSignup = ({ onRedirectToDashboard }) => {
  const [voter_Id, setVoterId] = useState('');
  const [action, setAction] = useState("Sign Up");
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [signupSuccess, setSignupSuccess] = useState(false);
  const [loginError, setLoginError] = useState('');
  const [,setLoginResponse] = useState(null); // State to store the login response

  const handleActionChange = (newAction) => {
    setAction(newAction);
    setVoterId('');
    setUsername('');
    setPassword('');
    setSignupSuccess(false);
    setLoginError(''); // Reset login error message
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `voter_Id=${voter_Id}&username=${username}&password=${password}`,
      });

      if (!response.ok) {
        throw new Error('Registration failed.');
      }

      setSignupSuccess(true);
    } catch (error) {
      console.error('Error during registration:', error);
      // Handle registration error, e.g., show an error message to the user
    }
  };

  const handleLogin = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `voter_Id=${voter_Id}&password=${password}`,
      });

      if (!response.ok) {
        // Handle HTTP errors
        const errorData = await response.json(); // Assuming the backend sends JSON error messages
        throw new Error(errorData.message || 'Login failed.');
      }

      const responseData = await response.json();
      console.log('Response data:', responseData);

      setLoginResponse(responseData); // Store the login response in state
      onRedirectToDashboard(responseData); // Pass the login response to Dashboard
    } catch (error) {
      console.error('Error during login:', error);
      setLoginError(error.message);
    }
  };
  
   
  
  
  return (
    <div className='container'>
      <div className="header">
        <div className="text">{action}</div>
        <div className="underline"></div>
      </div>

      {signupSuccess && (
        <div className="success-message">Signup successful! You can now login.</div>
      )}

      {loginError && (
        <div className="error-message">{loginError}</div>
      )}

      <div className="inputs">
        {action === "Login" ? null : (
          <div className="input">
            <img src={userIcon} alt="" />
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
        )}
        <div className="input">
          <img src={pancardIcon} alt="" />
          <input
            type="text"
            placeholder="Voter ID"
            value={voter_Id}
            onChange={(e) => setVoterId(e.target.value)}
          />
        </div>
        
        <div className="input">
          <img src={passwordIcon} alt="" />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
      </div>
      {action === "Sign Up" ? null : (
        <div className="new" onClick={() => handleActionChange("Sign Up")}>
          New User? <span>Click Here!</span>
        </div>
      )}
      {action === "Sign Up" ? (
        <div className="Already">
          Already a user? <span onClick={() => handleActionChange("Login")}>Click Here!</span>
        </div>
      ) : null}
      <div className="submit-container">
        <button className="submit" onClick={action === "Login" ? handleLogin : handleSubmit}>
          {action === "Login" ? "Login" : "Submit"}
        </button>
      </div>
      <div className="submit-container">
        <div
          className={action === "Login" ? "submit gray" : "submit"}
          onClick={() => handleActionChange("Sign Up")}
        >
          Sign Up
        </div>
        <div
          className={action === "Sign Up" ? "submit gray" : "submit"}
          onClick={() => handleActionChange("Login")}
        >
          Login
        </div>
      </div>
    </div>
  );
};

export default LoginSignup;
