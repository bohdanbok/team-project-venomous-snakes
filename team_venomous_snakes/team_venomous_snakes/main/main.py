from team_venomous_snakes.team_venomous_snakes.assistant import assistant
from team_venomous_snakes.team_venomous_snakes.notes import notes
from team_venomous_snakes.team_venomous_snakes.sort import sort
from team_venomous_snakes.team_venomous_snakes.weather import weather


def run_me():
    while True:
        print("Greeting, welcome to 'Venomous Snakes' assistant, please choose from the following options:\n"
              "1 - Assistant\n"
              "2 - Notes\n"
              "3 - Sort files\n"
              "4 - What is the weather?\n"
              "5 - Finish")
        request = input("What are we doing today?:").lower().strip()
        if request == "1":
            assistant.run_assistant()
        elif request == "2":
            notes.run_notes()
        elif request == "3":
            sort.sort_files()
        elif request == "4":
            weather.what_weather()
        elif request == "5":
            print("Was pleasure to work with you!")
            break


if __name__ == "__main__":
    run_me()
