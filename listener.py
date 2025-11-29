import threading

first_run = True

# .-=+=-* Real-time listener *-=+=-.
def start_listener(user_id, db):
    global first_run

    def callback(col_snapshot, changes, read_time):
        global first_run
        if first_run:
            first_run = False
            return

        for change in changes:
            doc = change.document.to_dict()
            if change.type.name == "ADDED":
                print(f"\n[Realtime Update] New note added: '{doc['title']}'")
            elif change.type.name == "MODIFIED":
                print(f"\n[Realtime Update] Note modified: '{doc['title']}'")
            elif change.type.name == "REMOVED":
                print(f"\n[Realtime Update] Note removed: '{doc['title']}'")

    notes_ref = db.collection("users").document(user_id).collection("notes")
    notes_ref.on_snapshot(callback)
