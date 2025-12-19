import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()
DB_NAME = os.getenv("DB_NAME")

def connect():
    connect = None
    try:
       connect = sqlite3.connect(DB_NAME)   
       print("Database connected successfully.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return connect
