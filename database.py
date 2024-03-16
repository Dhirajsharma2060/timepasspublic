from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Dhiraj%402060@localhost/fastapi"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Dhiraj@2060@localhost/fastapi"
# Encode the password
#encoded_password = urllib.parse.quote_plus("Dhiraj@2060")
# Construct the database URL with the encoded password
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:dhiraj123@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()