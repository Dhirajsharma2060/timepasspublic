# Face Recognition Voting System

This project is a **Face Recognition Voting System** built with **FastAPI**, **SQLAlchemy**, **OpenCV**, and **face_recognition**. It allows secure and seamless voting using facial recognition technology. The project also integrates with **Google Sheets** for counting votes.

## Features

### 1. Voter Registration
- **Voter ID**, username, and password registration.
- Face capture using a webcam and saved as a reference for future recognition.
- The system ensures each voter ID is unique and valid.

### 2. Login with Face Recognition
- Authenticate voters using their face.
- Voters must enter their Voter ID, password, and pass facial recognition to access the voting dashboard.
  
### 3. Voting
- Voters can cast their votes once, and the system updates the voter's status after voting.
- Tracks which party a voter has voted for.

### 4. Vote Counting
- Admin can view the total vote count for each party.
- Vote counts are updated in **Google Sheets** for transparency and easy access.

### 5. Admin Panel
- Admin login with credentials.
- Admin dashboard for managing voters and viewing vote counts.
- Admin can **search**, **update**, or **delete** voter details.

## Technology Stack

- **FastAPI**: Backend framework for building APIs.
- **SQLAlchemy**: ORM for handling database operations.
- **OpenCV**: For capturing images and performing face recognition.
- **face_recognition**: Library for comparing facial encodings.
- **Google Sheets API**: To store and display vote counts in real-time.

## Prerequisites

To run this project, you will need:

- Python 3.8+
- FastAPI
- SQLAlchemy
- OpenCV
- face_recognition
- Passlib (for password hashing)
- dotenv (for environment variables)
- gspread & oauth2client (for Google Sheets integration)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/face-recognition-voting-system.git
   cd face-recognition-voting-system
   ```
2. **Install Required Packages:**:   
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up Environment Variables**:   
   ```bash
   ADMIN_USERNAME=your_admin_username
   ADMIN_PASSWORD=your_admin_password
   ```
4. **Set Up Database:**:
Make sure you have the database configured. Adjust the database settings in the database.py file to match your setup.

5. **Google Sheets Integration:**:
- Enable the Google Sheets API and create credentials.
- Save your credentials as credential.json in the root directory.

6. **Run the Application:**:   
   ```bash
   uvicorn main:app --reload
   ```



