from auth import register_user, login_user
from db import init_db, add_note, get_notes, edit_note, delete_note
from listener import start_listener
import threading

db = init_db()

# .-=+=-* Authentication before showing main menu *-=+=-.
def authenticate():
    print("\n.-=+=-* Notes App *-=+=-.")
    print("Welcome! Choose an option:")
    print("1. Login")
    print("2. Register")
    choice = input("Option: ")

    user = None
    if choice == "1":
        user = login_user()
    elif choice == "2":
        user = register_user()

    if user:
        print("Authentication successful!\n")
        return user['localId']
    else:
        print("Exiting...")
        return None


#  CLI Menu *-=+=-.
def main_menu(user_id):
    while True:
        print("\n.-=+=-* Notes App Menu *-=+=-.")
        print("1. Add Note")
        print("2. View Notes")
        print("3. Update Note")
        print("4. Delete Note")
        print("5. Exit")

        choice = input("Choose an option (number): ")
        if choice not in ["1", "2", "3", "4", "5"]:
            print("Invalid choice. Please enter a number from 1 to 5.")
            continue

        if choice == "1":
            title = input("Enter note title: ")
            print("Enter note content (type 'END' on a new line to finish):")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == "END":
                    break
                lines.append(line)
            content = "\n".join(lines)  # join all lines with newline

            note_id = add_note(db, user_id, title, content)
            print(f"Note added with ID: {note_id}")
        
        elif choice == "2":
            notes = get_notes(db, user_id)
            if notes:
                for note in notes:
                    print(f"ID: {note['id']}")
                    print(note['title'].upper())
                    print(note['content'])
                    print("")
            else:
                print("No notes found.")
        
        elif choice == "3":
            note_id = input("Enter note ID to update: ")
            notes = get_notes(db, user_id)
            if note_id not in [note["id"] for note in notes]:
                print("Invalid note ID. Please try again.")
                continue
            edit_note(db, user_id, note_id)

        elif choice == "4":
            note_id = input("Enter note ID to delete: ")
            notes = get_notes(db, user_id)
            if note_id not in [note["id"] for note in notes]:
                print("Invalid note ID. Please try again.")
                continue
            delete_note(db, user_id, note_id)
            print("Note deleted.")

        elif choice == "5":
            print("Thanks for using the Notes App.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    user_id = authenticate()
    if user_id:
        # Start listener in a background thread
        listener_thread = threading.Thread(target=start_listener, args=(user_id, db), daemon=True)
        listener_thread.start()

        main_menu(user_id)