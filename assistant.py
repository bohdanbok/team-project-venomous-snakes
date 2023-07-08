import re
import pickle
from datetime import date, datetime
from collections import UserDict


class Field:
    def __init__(self, value=None):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass


class Name(Field):
    pass


class Phone(Field):
    PHONE_REGEX = re.compile(r"^\+?(\d{2})?\(?\d{3}\)?[\d\-\s]{7,10}$")

    def validate(self, phone):
        if not self.PHONE_REGEX.match(phone):
            raise ValueError(f"Phone number {phone} is invalid.")


class Birthday(Field):
    DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    def validate(self, date_str):
        if not self.DATE_REGEX.match(date_str):
            raise ValueError(f"Invalid date format: {date_str}. Expected format: YYYY-MM-DD.")

    @property
    def value(self):
        if self._value:
            return datetime.strptime(self._value, "%Y-%m-%d").date()
        return None

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value


class Email(Field):
    EMAIL_REGEX = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")

    def validate(self, email_str):
        if not self.EMAIL_REGEX.match(email_str):
            raise ValueError(f"Invalid email")

    @property
    def value(self):
        if self._value:
            return self._value
        return None

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value


class Record:
    def __init__(self, name, birthday=None, email=None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.email = email

    def add(self, phone):
        self.phones.append(phone)

    def days_to_birthday(self):
        if self.birthday and self.birthday.value:
            today = date.today()
            next_birthday = date(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left
        return None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        self.data.pop(name, None)

    def get_all_records(self):
        return self.data.values()

    def search(self, query):
        result = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower() or any(query in phone.value for phone in record.phones):
                result.append(record)
        return result


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except (IndexError, ValueError):
            return "Input Error.Please try one more time."
        except KeyError:
            return "No such contact, please try one more time."
    return inner


class Assistant:
    SAVE_FILE = "address_book.pickle"

    def __init__(self):
        self.address_book = AddressBook()

    @input_error
    def add(self, command_args):
        name = input("Write name: ")
        birthday = input("Please enter birthday (Format: YYYY-MM-DD): ")
        email = input("Please enter email:")
        record = Record(Name(name), Birthday(birthday), Email(email))
        phone = input("Enter phone number: ")
        record.add(Phone(phone))
        self.address_book.add_record(record)
        return "Contact was added."

    @input_error
    def change(self, command_args):
        name = command_args.strip()
        record = self.address_book.data.get(name)
        if not record:
            return "No such contact with phone number."
        phone = input("Enter new phone number: ")
        record.phones = [Phone(phone)]
        return "Result was saved."

    @input_error
    def phone(self, command_args):
        name = command_args.strip()
        record = self.address_book.data.get(name)
        if not record:
            return "No such contact with this phone number."
        return ', '.join([str(phone.value) for phone in record.phones])

    @input_error
    def show(self, command_args):
        return "\n".join([str(record.name.value) + ": " + ', '.join([str(phone.value) for phone in record.phones])
                          + (f", Email: {record.email.value}" if record.email else "")
                          + (f", Birthday: {record.birthday.value}" if record.email else "")
                          for record in self.address_book.get_all_records()])

    @input_error
    def birthday(self, command_args):
        name = command_args.strip()
        record = self.address_book.data.get(name)
        if not record:
            return "No such contact with this name."
        days = record.days_to_birthday()
        if days:
            return f"{days} left till birthday."
        else:
            return "There is no birthday day."

    @input_error
    def exit(self, command_args):
        self.save_data()
        return "See you in Assistant!"

    def load_data(self):
        try:
            with open(self.SAVE_FILE, "rb") as file:
                self.address_book = pickle.load(file)
        except FileNotFoundError:
            pass

    def save_data(self):
        with open(self.SAVE_FILE, "wb") as file:
            pickle.dump(self.address_book, file)


if __name__ == "__main__":
    assistant = Assistant()
    assistant.load_data()
    while True:
        print("Greeting, welcome to 'Venomous Snakes' assistant, please choose from the following options:\n"
              "1 - Assistant\n"
              "2 - Notes\n"
              "3 - Sort files\n"
              "4 - Finish")
        request = input("What are we doing today?:")
        if request == "1":
            print("Welcome to Assistant! I know such commands:\n"
                  "Add - Adding new Person to Contacts\n"
                  "Change {name}- Changing existing phone for contact \n"
                  "Phone {name} - Showing phone for person\n"
                  "Show - Show all contacts in AddressBook\n"
                  "Birthday {name} - How many days till Birthday \n"
                  "Exit - Close Assistant \n")
            while True:
                command = input(">>> ")
                command_name, command_args = command.split(" ", 1) if " " in command else (command, "")
                function = getattr(assistant, command_name.lower(), None)
                if function:
                    print(function(command_args))
                else:
                    print("Unknown command - please try one more time.")
                if command_name == 'exit':
                    break
        elif request == "2":
            # Will be added logic for notes
            pass
        elif request == "3":
            # Will be added logic for sorting
            pass
        elif request == "4":
            print("Was pleasure to work with you!")
            break
