import firebase_admin
from firebase_admin import credentials, firestore

#db connection
def init_db():
    cred = credentials.Certificate("service-account.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firestore.client()

#Create note
def add_note(db, title, content):
    doc_ref = db.collection("notes").document()  #creating a reference for where the document is stored in the notes collection
    doc_ref.set({
        "title": title,
        "content": content
    })
    return doc_ref.id

#Get all notes
def get_notes(db):
    notes_ref = db.collection("notes").stream()  #getting all the documents from the collection
    notes = []
    for doc in notes_ref:
        data = doc.to_dict()
        data["id"] = doc.id
        notes.append(data)
    return notes

#Update note
def edit_note(db, note_id):
    doc_ref = db.collection("notes").document(note_id)
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
            line_num = int(input("Enter line number to remove: "))
            if 1 <= line_num <= len(lines):
                lines.pop(line_num - 1)
                doc_ref.update({"content": "\n".join(lines)})
            else:
                print("Invalid line number.")
        
        print("Content updated!")


#Delete note
def delete_note(db, note_id):
    db.collection("notes").document(note_id).delete()
