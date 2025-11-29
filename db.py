import firebase_admin
from firebase_admin import credentials, firestore

# .-=+=-* db connection *-=+=-.
def init_db():
    """
    Initialize connection to Firestore using a service account.

    Returns:
        firestore.client: A Firestore client object to interact with the database.
    """
    cred = credentials.Certificate("service-account.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firestore.client()

#Create note
def add_note(db, user_id, title, content):
    """
    Add a new note to a specific user's collection.

    Args:
        db (firestore.client): Firestore client object.
        user_id (str): ID of the logged-in user.
        title (str): Title of the note.
        content (str): Content of the note.

    Returns:
        str: ID of the newly created note.
    """
    doc_ref = db.collection("users").document(user_id).collection("notes").document()  #creating a reference for where the document is stored in the notes collection for each user
    doc_ref.set({
        "title": title,
        "content": content
    })
    return doc_ref.id

#Get all notes
def get_notes(db, user_id):
    """
    Retrieve all notes for a specific user.

    Args:
        db (firestore.client): Firestore client object.
        user_id (str): ID of the logged-in user.

    Returns:
        list: A list of dictionaries, each containing note data with its ID.
    """
    notes_ref = db.collection("users").document(user_id).collection("notes").stream()  #getting all the documents from the collection
    notes = []
    for doc in notes_ref:
        data = doc.to_dict()
        data["id"] = doc.id
        notes.append(data)
    return notes

#Update note
def edit_note(db, user_id, note_id):
    """
    Update an existing note's title or content for a specific user.

    Args:
        db (firestore.client): Firestore client object.
        user_id (str): ID of the logged-in user.
        note_id (str): ID of the note to edit.

    Returns:
        None
    """
    doc_ref = db.collection("users").document(user_id).collection("notes").document(note_id)
    doc = doc_ref.get()

    if not doc.exists:
        print("Note not found.")
        return

    current_data = doc.to_dict()
    print(f"\nCurrent Title: {current_data['title']}")
    print("Current Content:\n", current_data["content"])

    print("\nOptions:")
    print("1. Edit title")
    print("2. Edit content")
    choice = input("Choose an option: ")
    if choice not in ["1", "2"]:
        print("Invalid option. Please select 1 or 2.")
        return

    if choice == "1":
        new_title = input("Enter new title: ")
        doc_ref.update({"title": new_title})
        print("Title updated!")

    elif choice == "2":
        print("\nContent editing options:")
        print("a. Append text")
        print("b. Replace content")
        print("c. Remove a line")
        sub_choice = input("Choose an option: ")
        if sub_choice.lower() not in ["a", "b", "c"]:
            print("Invalid option. Choose a, b, or c.")
            return

        if sub_choice.lower() == "a":
            new_text = input("Text to append: ")
            updated_content = current_data["content"] + "\n" + new_text
            doc_ref.update({"content": updated_content})

        elif sub_choice.lower() == "b":
            new_text = input("Enter new content: ")
            doc_ref.update({"content": new_text})

        elif sub_choice.lower() == "c":
            lines = current_data["content"].split("\n")
            for i, line in enumerate(lines, 1):
                print(f"{i}: {line}")
            line_num = input("Enter line number to remove: ")
            if not line_num.isdigit():
                print("Please enter a valid number.")
                return
            line_num = int(line_num)
            if 1 <= line_num <= len(lines):
                lines.pop(line_num - 1)
                doc_ref.update({"content": "\n".join(lines)})
            else:
                print("Invalid line number.")
        
        print("Content updated!")


#Delete note
def delete_note(db, user_id, note_id):
    """
    Delete a note from a specific user's collection.

    Args:
        db (firestore.client): Firestore client object.
        user_id (str): ID of the logged-in user.
        note_id (str): ID of the note to delete.

    Returns:
        None
    """
    db.collection("users").document(user_id).collection("notes").document(note_id).delete()
