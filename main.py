from db import init_db, add_note, get_notes, edit_note, delete_note
import threading

db = init_db()

first_run = True

# .-=+=-* Real-time listener *-=+=-.
def on_notes_update(col_snapshot, changes, read_time):
    global first_run
    if first_run:
        first_run = False
        return  # skip the initial load

    for change in changes:
        doc = change.document.to_dict()
        if change.type.name == "ADDED":
            print(f"\n[Realtime Update] New note added: '{doc['title']}'")
        elif change.type.name == "MODIFIED":
            print(f"\n[Realtime Update] Note modified: '{doc['title']}'")
        elif change.type.name == "REMOVED":
            print(f"\n[Realtime Update] Note removed: '{doc['title']}'")

def start_listener():
    notes_ref = db.collection("notes")
    notes_ref.on_snapshot(on_notes_update)

# Start listener in a background thread
listener_thread = threading.Thread(target=start_listener, daemon=True)
listener_thread.start()

# .-=+=-* CLI Menu *-=+=-.
def main_menu():
    while True:
        print("\n===== Notes App Menu =====")
        print("1. Add Note")
        print("2. View Notes")
        print("3. Update Note")
        print("4. Delete Note")
        print("5. Exit")

        choice = input("Choose an option (number): ")

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

            note_id = add_note(db, title, content)
            print(f"Note added with ID: {note_id}")
        
        elif choice == "2":
            notes = get_notes(db)
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
            edit_note(db, note_id)

        elif choice == "4":
            note_id = input("Enter note ID to delete: ")
            delete_note(db, note_id)
            print("Note deleted.")

        elif choice == "5":
            print("Thanks for using the Notes App.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()