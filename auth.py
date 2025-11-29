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
    """
    Register a new user with email and password using Firebase Authentication.

    Prompts the user to input:
        - Email
        - Password

    Returns:
        dict: A dictionary containing user information if registration is successful.
        None: If registration fails.
    """
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
    """
    Log in an existing user with email and password using Firebase Authentication.

    Prompts the user to input:
        - Email
        - Password

    Returns:
        dict: A dictionary containing user information if login is successful.
        None: If login fails.
    """
    email = input("Enter email: ")
    password = input("Enter password: ")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print("Logged in successfully!")
        return user
    except Exception as e:
        print("Error:", e)
        return None