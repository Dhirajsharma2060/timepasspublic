from fastapi import Depends, FastAPI, Form, HTTPException, Request
import face_recognition
import cv2
import os 
from dotenv import load_dotenv
import numpy as np
from sqlalchemy import func
#from fastapi.templating import TemplateResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from database import SessionLocal, engine
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from test import test_conn
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from models import Voter
from connect import connect
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
#from websocket_manager import WebSocketManager
import models
import core
models.Base.metadata.create_all(bind=engine)
load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates") 
app.add_middleware(core.create_cors_middleware)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
test_conn()
conn, cursor = connect()    
   

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# In-memory data structure to store user data and face encoding
#my_data = {}
# Define the scope and credentials for accessing Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
client = gspread.authorize(credentials)


conn,cursor=connect()
def is_valid_voter_Id(voter_Id: int) -> bool:
    return len(str(voter_Id)) == 10
def is_voter_Id_taken(voter_Id: int, session: Session) -> bool:
    try:
        # Check if the voter_Id exists in the 'voter' table using SQLAlchemy ORM
        return session.query(Voter).filter(Voter.voter_id == voter_Id).first() is not None

    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        print(f"Error checking if voter_Id is taken: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def capture_and_save_image(voter_Id: str):
    folder_path="imageref"
    os.makedirs(folder_path, exist_ok=True)
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        cv2.putText(frame, "Press 's' to capture your image", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('Capture Your Image', frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            image_filename = os.path.join(folder_path,f"{voter_Id}_image.jpg")
            cv2.imwrite(image_filename, frame)
            cv2.putText(frame, "Image Captured and Saved", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            break

    video_capture.release()
    cv2.destroyAllWindows()

    reference_image = face_recognition.load_image_file(image_filename)
    reference_encoding = face_recognition.face_encodings(reference_image)[0]

    return reference_encoding
def recognize_face(voter_Id: str):
    folder_path = "imageref"
    reference_filename = os.path.join(folder_path, f"{voter_Id}_image.jpg")
    reference_image = cv2.imread(reference_filename)
    reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
    reference_face_locations = face_recognition.face_locations(reference_image)
    reference_encodings = face_recognition.face_encodings(reference_image, reference_face_locations, model='small')

    if len(reference_encodings) == 0:
        print("Error: Failed to encode reference face.")
        return False

    reference_encoding = reference_encodings[0]

    video_capture = cv2.VideoCapture(0)
    distance = float('inf')  # Initialize distance with a default value

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(frame_rgb)
        
        if len(face_locations) > 0:
            face_encodings = face_recognition.face_encodings(frame_rgb, face_locations, model='small')
            if len(face_encodings) > 0:
                face_encoding = face_encodings[0]
                distance = np.linalg.norm(reference_encoding - face_encoding)

                if distance < 0.6:  # Adjust threshold for accurate matching
                    cv2.putText(frame, f"Match Found for {voter_Id}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, "Please press Q", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, f"No Match for {voter_Id}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(frame, "Face does not match", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    break  # Exit the loop if face does not match

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    return distance < 0.6  # Return True if match found

def is_valid_voter_Id(voter_Id: int) -> bool:
    return len(str(voter_Id)) == 10
#@app.get("/")
#async def landing():
#  print("Welcome !!!! the backend ")  
#  return{"Welcome"}
@app.get("/register")
async def get_data(db: Session = Depends(get_db)):
    #cursor.execute("""
      #              SELECT voter_Id ,password FROM voter
     #              """)
    #posts=cursor.fetchall()
    posts=db.query(models.Voter).all()
    return{"data":posts}
@app.get("/sqlalchemy")
async def test_post(db: Session = Depends(get_db)):
    posts=db.query(models.Voter).all()
    return{"success":posts}
# Registration page with face recognition

@app.post("/register")

async def register(
    voter_Id: int = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
   
    # Check if the voter_Id is already taken (you should implement this function)
    if is_voter_Id_taken(voter_Id,db):
        raise HTTPException(status_code=400, detail="voter_Id already taken")

    # Check if the voter_Id has a valid length
    if not is_valid_voter_Id(voter_Id):
        raise HTTPException(status_code=400, detail="Invalid voter_Id length. It should be of length 10.")

    # Connect to the database
    conn, cursor = connect()


    try:
        hashed_password=pwd_context.hash(password)
        
        reference_encoding = capture_and_save_image(voter_Id)
        # Insert user data into the 'post' table
        #cursor.execute(
         #   "INSERT INTO voter (voter_Id, username, password) VALUES (%s, %s, %s) RETURNING *;",
          #  (voter_Id, username,hashed_password),
        #)
        new_voter = Voter(voter_id=voter_Id, name=username, password=hashed_password)
        db.add(new_voter)

        db.commit()
        db.refresh(new_voter)


        # Fetch the inserted data
        #new_post = cursor.fetchone()

        # Commit the changes to the database
        #conn.commit()

        # Capture and save the image, get the face encoding
        #reference_encoding = capture_and_save_image(voter_Id)

        # You may want to insert the face_encoding into another table

        # Return a success message
        print("Redirecting to login page...")
        #return RedirectResponse(url="http://127.0.0.1:5500/templates/login.html")
        #return RedirectResponse("http://127.0.0.1:5500/templates/login.html")
        return("Sucess")
        

    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        print(f"Error during registration: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        # Close the database connection and cursor
        if conn is not None:
            conn.close()
        if cursor is not None:
            cursor.close()
    


# Login page with face recognition
#@app.get("/login", response_class=HTMLResponse)
#async def read_login(request: Request):
    #return ("login.html", {"request": request})

@app.post("/login")
async def login(
    voter_Id: int = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_data = db.query(models.Voter).filter(models.Voter.voter_id == voter_Id).first()
    
    if user_data:
        if recognize_face(voter_Id):
            if pwd_context.verify(password, user_data.password):
                return RedirectResponse(url=f"/dashboard/{voter_Id}",status_code=303)
            else:
                raise HTTPException(status_code=401, detail="Incorrect password. Please check.")
        else:
            raise HTTPException(status_code=401, detail="Face recognition failed.")
    else:
        raise HTTPException(status_code=404, detail="User not found.")

@app.get("/dashboard/{voter_Id}", response_class=HTMLResponse)
async def dashboard(
    voter_Id: int,
    db: Session = Depends(get_db)
):
    user = db.query(models.Voter).filter(models.Voter.voter_id == voter_Id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    voting_status = "Voted" if user.status else "Not Voted"

    data = {
        "voter_Id": user.voter_id,
        "name": user.name,
        "status": voting_status,
    }
    return JSONResponse(data)
#@app.get("/logout")
#async def logout(session: Session = Depends(get_db)):
 #   session.close()  # Close the session
  #  return RedirectResponse(url="/")
#from fastapi.templating import Jinja2Templates

#templates = Jinja2Templates(directory="templates")

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
@app.post("/vote/{voter_Id}/{party}")
async def vote(
    voter_Id: int,
    party: str,
    db: Session = Depends(get_db)
):
    # Check if the voter exists
    voter = db.query(Voter).filter(Voter.voter_id == voter_Id).first()
    if voter is None:
        raise HTTPException(status_code=404, detail="Voter not found")

    # Check if the voter has already voted
    if voter.status:
        raise HTTPException(status_code=400, detail="Voter has already voted")

    # Update the voter's status to indicate that they have voted
    voter.status = True
    # Update the voted party for the voter
    voter.voted_party = party

    # Commit the changes to the database
    db.commit()

    return {"message": f"Vote for {party} recorded successfully"}

@app.put("/users/{voter_id}")
async def get_update_user(voter_id: int, new_data: dict, db: Session = Depends(get_db)):
    # Fetch the user from the database
    user = db.query(Voter).filter(Voter.voter_id == voter_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Show the current user information
    user_info = {
        "voter_id": user.voter_id,
        "name": user.name,
        # Add more fields as needed
    }

    # Update user information based on the new_data dictionary
    for key, value in new_data.items():
        setattr(user, key, value)

    # Commit the changes to the database
    db.commit()

    return {"message": "User information updated successfully", "user_info": user_info}

# Endpoint to delete a user
@app.delete("/users/{voter_id}")
async def delete_user(voter_id: int, db: Session = Depends(get_db)):
    # Fetch the user from the database
    user = db.query(Voter).filter(Voter.voter_id == voter_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user from the database
    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
# Endpoint for changing password (forgot password)
@app.post("/forgot-password")
async def forgot_password(
    voter_id: int = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Fetch the user from the database
    user = db.query(Voter).filter(Voter.voter_id == voter_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if the face matches
    if not recognize_face(str(voter_id)):
        raise HTTPException(status_code=401, detail="Face recognition failed.")


    # Check if the new password and confirm password match
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Hash the new password
    hashed_password = pwd_context.hash(new_password)

    # Update the user's password in the database
    user.password = hashed_password
    db.commit()

    return {"message": "Password updated successfully"}
@app.get("/count-votes")
async def count_votes(db: Session = Depends(get_db)):
    # Query the database to get the count of votes for each party
    vote_counts = db.query(Voter.voted_party, func.count(Voter.voter_id)).filter(Voter.voted_party !=None).group_by(Voter.voted_party).all()

    # Prepare the response data
    result = {}
    for party, count in vote_counts:
        result[party] = count

    # Update Google Sheets with the vote counts
    spreadsheet = client.open('counting_votes')
    worksheet = spreadsheet.get_worksheet(0)  # Assuming data is in the first sheet
    worksheet.clear()  # Clear existing data
    header_row = ['Party', 'Votes']  # Assuming column headers
    worksheet.append_row(header_row)  # Add header row
    for party, count in result.items():
        worksheet.append_row([party, count])  # Append party and vote count

    return result
@app.get("/search-voter/{voter_Id}")
async def search_voter(voter_Id: int, db: Session = Depends(get_db)):
    # Query the database to search for the voter by their voter ID
    voter = db.query(Voter).filter(Voter.voter_id == voter_Id).first()

    if voter:
        # If the voter is found, return their details
        return {
            "voter_Id": voter.voter_id,
            "name": voter.name,
            "status": "Voted" if voter.status else "Not Voted"
        }
    else:
        # If the voter is not found, raise an HTTPException with a 404 status code
        raise HTTPException(status_code=404, detail="Voter not found")


# Create Jinja2Templates instance
templates = Jinja2Templates(directory="templates")
# Define routes
@app.get("/")
async def landing(request:Request):
  #print("Welcome !!!! the backend ")  
  #return{"Welcome"}
  return templates.TemplateResponse("adminlogin.html",{"request":request})
@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login(request: Request):
    return templates.TemplateResponse("adminlogin.html", {"request": request})

#admin credential 
#admin_credentials = {"admin@2024": "401104"}
# Get admin credentials from environment variables
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
admin_credentials={os.getenv("ADMIN_USERNAME"):os.getenv("ADMIN_PASSWORD")}
#@app.post("/admin-login", response_class=HTMLResponse)
#async def admin_login(username: str = Form(...), password: str = Form(...)):
 #   if username in admin_credentials and password == admin_credentials[username]:
  #      # Admin authentication successful
   #     response = Response(content="Admin login successful. You have access to admin privileges.")
    #    response.headers["HX-Trigger"] = "result"
     #   response.headers["HX-Scroll-Target"] = "#result"
      #  return response
    #else:
     #   raise HTTPException(status_code=401, detail="Invalid credentials. Access denied.")
@app.post("/admin-login", response_class=HTMLResponse)
async def admin_login(username: str = Form(...), password: str = Form(...)):
    if username in admin_credentials and password == admin_credentials[username]:
        # Admin authentication successful, redirect to admin dashboard
        return RedirectResponse(url="/admin/dashboard", status_code=303)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials. Access denied.")
@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("admindashboard.html", {"request": request})

@app.get("/admin/search", response_class=HTMLResponse)
async def admin_search(request: Request):
    return templates.TemplateResponse("search-voter.html", {"request": request})    

# Update voter endpoint
@app.get("/admin/update", response_class=HTMLResponse)
async def admin_update(request: Request):
    return templates.TemplateResponse("update-voter.html", {"request": request})

# Delete voter endpoint
@app.get("/admin/delete", response_class=HTMLResponse)
async def admin_delete(request: Request):
    return templates.TemplateResponse("delete-voter.html", {"request": request})
@app.post("/search-voter/{voter_Id}")
async def search_voter(voter_Id: str, db: Session = Depends(get_db)):
    # Query the database to search for the voter by their voter ID
    voter = db.query(Voter).filter(Voter.voter_id == voter_Id).first()

    if voter:
        # If the voter is found, return their details
        return {
            "voter_Id": voter.voter_id,
            "name": voter.name,
            "status": "Voted" if voter.status else "Not Voted"
        }
    else:
        # If the voter is not found, raise an HTTPException with a 404 status code
        raise HTTPException(status_code=404, detail="Voter not found")
@app.get("/admin/logout")
async def logout():
    # Here you can implement any logout logic, such as clearing session data, etc.
    # For simplicity, let's assume logging out just redirects to the login page
    return RedirectResponse(url="/admin/login", status_code=303)
@app.get("/admin/count-votes", response_class=HTMLResponse)
async def count_votes(request: Request, db: Session = Depends(get_db)):
    # Logic to count votes goes here
    # For demonstration purposes, let's assume you have a function to count votes
    total_votes = db.query(models.Voter.voted_party, func.count(models.Voter.voter_id)).filter(models.Voter.voted_party != None).group_by(models.Voter.voted_party).all()
    
    # Convert SQLAlchemy Rows to list of dictionaries
    total_votes_json = [{"voted_party": party, "total_votes": count} for party, count in total_votes]
    
    return templates.TemplateResponse("countvote.html", {"request": request, "total_votes": total_votes_json})
