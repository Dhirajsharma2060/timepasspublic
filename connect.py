import time
import psycopg2
from psycopg2.extras import RealDictCursor
import os 

def connect():
    while True:
        try:
            host = os.getenv("HOST")
            database = os.getenv("DATABASE")
            user = os.getenv("USER")
            password = os.getenv("PASSWORD")
            conn=psycopg2.connect(host=host,database=database ,user=user,password=password,cursor_factory=RealDictCursor)
            cursor=conn.cursor()
            print("successfully connected to database")
            return conn, cursor
        except Exception as error: 
            print("failed to connect with database") 
            print("Error:",error) 
            time.sleep(2)    