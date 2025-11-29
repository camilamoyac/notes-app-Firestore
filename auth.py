import os
from dotenv import load_dotenv
import pyrebase

load_dotenv()

config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": "",
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": os.getenv("FIREBASE_APP_ID")
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def register_user():
    email = input("Enter email: ")
    password = input("Enter password: ")
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print("User registered successfully!")
        return user
    except Exception as e:
        print("Error:", e)
        return None

def login_user():
    email = input("Enter email: ")
    password = input("Enter password: ")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print("Logged in successfully!")
        return user
    except Exception as e:
        print("Error:", e)
        return None