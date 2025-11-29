# Overview

This project is a Python-based Notes App designed to help users create, view, update, and delete personal notes while storing them securely in a cloud database. The app integrates with Google Firebase Firestore, allowing real-time updates so that any changes to notes are instantly reflected in the application. Users can add multi-line notes, edit titles or content, remove specific lines, and receive notifications when notes are added, modified, or deleted.

The purpose of this software is to further my learning as a software engineer by practicing cloud integration, real-time data handling, and user authentication. It also demonstrates the ability to build a fully functional command-line interface (CLI) application that interacts with a NoSQL cloud database.

[Software Demo Video](http://youtube.link.goes.here)

# Cloud Database

This application uses Google Firebase Firestore as its cloud database. Firestore is a NoSQL database that stores data in flexible, schema-less documents grouped into collections.  

The database structure is as follows:
- `users` collection: Each user is stored as a document identified by their unique `user_id`.
    - `notes` subcollection: Contains all notes for that user. Each note document has the following fields:
        - `title`: The title of the note
        - `content`: The content of the note, supporting multiple lines

This structure allows each user to have isolated notes and supports real-time updates for any changes.

# Development Environment

- **Programming Language:** Python 3.10
- **Libraries/Tools:**
  - `firebase-admin` for interacting with Firestore
  - `pyrebase` for user authentication
  - Standard Python libraries: `threading` for real-time updates
- **Editor:** Visual Studio Code
- **Other Tools:** OBS Studio and YouTube for the app demonstration

# Useful Websites

{Make a list of websites that you found helpful in this project}

- [Firebase Documentation](https://firebase.google.com/docs/firestore/quickstart)
- [Firebase Documentation](https://firebase.google.com/docs/auth/where-to-start)
- [Pyrebase Documentation](https://github.com/thisbejim/Pyrebase)
- [Python Documentation](https://docs.python.org/3/)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}

- Implement more user-friendly IDs for notes
- Build a GUI or web interface for the app
- Add optional tagging or categorization for notes