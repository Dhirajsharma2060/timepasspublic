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
  const [,setLoginResponse] = useState(null);
  const [new_password,setNewPassword]=useState('');
  const [confirm_password,setConfirmPassword]=useState('');
  const [forgetpasswordSuccess,setForgetpasswordSuccess]=useState(false); // State to store the forget password success status
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [passwordChanged, setPasswordChanged] = useState(false);

  const handleActionChange = (newAction) => {
    setAction(newAction);
    setVoterId('');
    setUsername('');
    setPassword('');
    setSignupSuccess(false);
    setLoginError(''); // Reset login error message
    setForgetpasswordSuccess(false); // Reset forget password success status
    setPasswordChanged(false); // Reset password changed status
    setShowConfirmation(false); // Hide confirmation dialog
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Validation logic for signup
    if (!voter_Id || !username || !password) {
      setLoginError('Please fill in all required fields.');
      return;
    }
    if (!/^[a-zA-Z][a-zA-Z0-9]*$/.test(username)) {
      setLoginError('Username should start with a letter and contain only letters and numbers.');
      return;
    }
    if (password.startsWith('0')) {
      setLoginError('Password should not start with zero.');
      return;
    }
    // Submit logic for signup
    
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
      // Validation for login
      if (!voter_Id || !password) {
        setLoginError('Please fill in Voter ID and password.');
        return;
      }
      const response = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `voter_Id=${voter_Id}&password=${password}`,
      });

      if (!response.ok) {
      // Handle HTTP errors
      const errorData = await response.json();
      if (errorData.message === 'Voter not found') {
        setLoginError('Voter not found. Please check your Voter ID.');
      } else {
        throw new Error(errorData.message || 'Login failed.');
      }
    } else {
      const responseData = await response.json();
      console.log('Response data:', responseData);

      setLoginResponse(responseData); // Store the login response in state
      onRedirectToDashboard(responseData); // Pass the login response to Dashboard
    }
  } catch (error) {
    console.error('Error during login:', error);
    setLoginError(error.message || 'An error occurred during login.');
  }
};

  const handleForgetPasswordClick = () => {
    setShowConfirmation(true);
  };

  const handleForgetPasswordConfirm = () => {
    setForgetpasswordSuccess(true);
    setShowConfirmation(false);
  };

  const handleForgetPasswordCancel = () => {
    setShowConfirmation(false);
  };

  const handleForgetPassword = async () => {
    try {
      // Validate passwords before sending request
      if (new_password !== confirm_password) {
        throw new Error('New password and confirm password do not match.');
      }

      // Check if fields are empty
      if (!voter_Id || !new_password || !confirm_password) {
        throw new Error('Please fill in all required fields.');
      }

      const response = await fetch('http://127.0.0.1:8000/forgot-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `voter_id=${voter_Id}&new_password=${new_password}&confirm_password=${confirm_password}`,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Password reset failed.');
      }

      setPasswordChanged(true); // Set password changed status to true
    } catch (error) {
      console.error('Error during changing password:', error);
      setLoginError(error.message); // Consider using a separate state for forget password errors
    }
  };

  const handleForgetPasswordClose = () => {
    setForgetpasswordSuccess(false);
  };

  return (
    <div className='container'>
      <div className="header">
        <div className="text">{action}</div>
        <div className="underline"></div>
      </div>

      {signupSuccess && (
        <div className="success-message" style={{color:'green'}}>Signup successful! You can now login.</div>
      )}

      {loginError && (
        <div className="error-message" style={{color:'red'}}>{loginError}</div>
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
      {action === "Sign Up" ? null : (
        <div className="forgot-container">
          <div className="forgot" onClick={handleForgetPasswordClick}>
            Forgot Password? <span>Click Here!</span>
          </div>
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

      {showConfirmation && (
        <div className="confirmation-dialog">
          <div className="confirmation-message">
            Are you sure you want to reset your password?
          </div>
          <div className="confirmation-buttons">
            <button onClick={handleForgetPasswordConfirm}>Yes</button>
            <button onClick={handleForgetPasswordCancel}>No</button>
          </div>
        </div>
      )}

      {passwordChanged && (
        <div className="success-message">Password changed successfully! Redirecting to login page...</div>
      )}

      {forgetpasswordSuccess && (
        <div className="forgot-password-form">
          <div className="close-button" onClick={handleForgetPasswordClose}>Close</div> {/* Close button */}
          <h2>Forgot Password?</h2>
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
              placeholder="New Password"
              value={new_password}
              onChange={(e) => setNewPassword(e.target.value)}
            />
          </div>
          <div className="input">
            <img src={passwordIcon} alt="" />
            <input
              type="password"
              placeholder="Confirm Password"
              value={confirm_password}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </div>
          <button className="submit" onClick={handleForgetPassword}>
            Submit
          </button>
        </div>
      )}
    </div>
  );
};

export default LoginSignup;
