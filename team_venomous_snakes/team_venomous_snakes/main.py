from .assistant.assistant import run_assistant
from .notes.notes import run_notes
from .sort.sort import sort_files
from .weather.weather import what_weather


def run():
    while True:
        print("Greeting, welcome to 'Venomous Snakes' assistant, please choose from the following options:\n"
              "1 - Assistant\n"
              "2 - Notes\n"
              "3 - Sort files\n"
              "4 - What is the weather?\n"
              "5 - Finish")
        request = input("What are we doing today?:").lower().strip()
        if request == "1":
            run_assistant()
        elif request == "2":
            run_notes()
        elif request == "3":
            sort_files()
        elif request == "4":
            what_weather()
        elif request == "5":
            print("Was pleasure to work with you!")
            break


if __name__ == "__main__":
    run()
