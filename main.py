from re import template
from fastapi import Depends, FastAPI, Form, HTTPException, Request, WebSocket, WebSocketDisconnect, requests
import face_recognition
import cv2
import os 
from dotenv import load_dotenv
from core import create_cors_middleware
#from fastapi.templating import TemplateResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from database import SessionLocal, engine
from test import test_conn
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from models import Voter
from connect import connect
from fastapi import FastAPI, Depends, WebSocket
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
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
    video_capture = cv2.VideoCapture(0)

    # Load the reference image and compute its encoding
    reference_filename = os.path.join(folder_path, f"{voter_Id}_image.jpg")
    reference_image = face_recognition.load_image_file(reference_filename)
    reference_encoding = face_recognition.face_encodings(reference_image)[0]

    while True:
        # Capture a frame from the webcam
        ret, frame = video_capture.read()

        # Find face locations in the frame
        face_locations = face_recognition.face_locations(frame)

        if len(face_locations) > 0:
            # Encode the detected face
            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

            # Compare the detected face encoding with the reference encoding
            results = face_recognition.compare_faces([reference_encoding], face_encoding)

            # Display recognition result
            if results[0]:
                cv2.putText(frame, f"Match Found for {voter_Id}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, "Please press Q", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, f"No Match for {voter_Id}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                return False
    

        # Display the frame
        cv2.imshow('Face Recognition', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the OpenCV window
    video_capture.release()
    cv2.destroyAllWindows()
    return True

def is_valid_voter_Id(voter_Id: int) -> bool:
    return len(str(voter_Id)) == 10
@app.get("/")
async def landing():
  print("Welcome !!!! the backend ")  
  return{"Welcome"}
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
@app.get("/logout")
async def logout(session: Session = Depends(get_db)):
    session.close()  # Close the session
    return RedirectResponse(url="/")
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
