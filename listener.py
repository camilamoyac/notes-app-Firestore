import threading

first_run = True

# .-=+=-* Real-time listener *-=+=-.
def start_listener(user_id, db):
    """
    Start a real-time listener on the logged-in user's notes collection.

    The listener prints updates to the console whenever a note is added,
    modified, or deleted. Skips the initial loading of existing notes.

    Args:
        user_id (str): ID of the logged-in user.
        db (firestore.client): Firestore client object.

    Returns:
        None
    """
    global first_run

    def callback(col_snapshot, changes, read_time):
        """
        Callback function triggered by Firestore on changes in the notes collection.

        Args:
            col_snapshot (list): List of DocumentSnapshot objects representing the current state of the collection.
            changes (list): List of DocumentChange objects representing the changes.
            read_time (datetime): The time at which the snapshot was read.

        Returns:
            None
        """
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
