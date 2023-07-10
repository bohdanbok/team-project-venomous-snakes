import pickle


class Notes:
    SAVE_FILE = "notes.pickle"

    def __init__(self):
        self.notes = []

    def create(self):
        note_name = input("Please write note name: ")
        note_text = input("Please write your note here: ")
        self.notes.append({f"{note_name}": [note_text, []]})
        return "Note was created!"

    def search(self):
        keyword = input("Please write your key word here: ")
        matching_notes = []
        for note in self.notes:
            for name, value in note.items():
                if keyword in name or keyword in value[0] or keyword in value[1]:
                    matching_notes.append(note)
        return matching_notes

    def edit(self):
        note_index = int(input("Please write what note you are willing to edit:")) - 1
        if note_index < len(self.notes):
            print(self.notes[note_index])
            new_text = input("Please write new text for this note: ")
            for key, value in self.notes[note_index].items():
                self.notes[note_index][f"{key}"][0] = new_text
            return "Note was edited"
        else:
            return "No note with such number"

    def show(self):
        return self.notes

    def delete(self):
        note_index = int(input("Please write number, which note you are willing to delete:")) - 1
        if note_index < len(self.notes):
            del self.notes[note_index]
            return "Note was deleted"
        return "No note with such index"

    def tag(self):
        note_index = int(input("Please write number, which note you are willing to tag:")) - 1
        tags = input("Please write Tag:")
        if note_index < len(self.notes):
            for key, value in self.notes[note_index].items():
                self.notes[note_index][f"{key}"][1].append(tags)
            return "Tag was added!"
        return "No note with such index"

    def exit(self):
        self.save()
        return "See you in Note Assistant!"

    def load_data(self):
        try:
            with open(self.SAVE_FILE, "rb") as file:
                self.notes = pickle.load(file)
        except FileNotFoundError:
            pass

    def save(self):
        with open(self.SAVE_FILE, "wb") as file:
            pickle.dump(self.notes, file)
        return "Was saved!"


def run_notes():
    notes = Notes()
    notes.load_data()
    print("Welcome to notes assistant! I know such commands:\n"
          "Create - Creating new note\n"
          "Search - Searching info in note\n"
          "Edit - Edit existing note\n"
          "Show - Showing what notes was created\n"
          "Delete - Deleting note\n"
          "Tag - Adding tag to note\n"
          "Save - Saving information\n"
          'Exit - Close note assistant')
    while True:
        print("Commands: Create, Search, Edit, Delete, Tag, Save, Exit")
        command = input(">>> ")
        function = getattr(notes, command.lower().strip(), None)
        if function:
            print(function())
        else:
            print("Unknown command - please try one more time.")
        if command == 'exit':
            print("See you!")
            break


if __name__ == "__main__":
    run_notes()
