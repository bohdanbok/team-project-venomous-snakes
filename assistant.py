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


class Address(Field):
    pass


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
    def __init__(self, name, address=None, birthday=None, email=None):
        self.name = name
        self.phones = []
        self.address = address
        self.birthday = birthday
        self.email = email

    def add(self, phone):
        self.phones.append(phone)

    def set_birthday(self, birthday):
        self.birthday = birthday

    def set_email(self, email):
        self.email = email

    def set_address(self, address):
        self.address = address

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
    def create(self):
        name = input("Write name: ")
        record = Record(Name(name))
        phone = input("Enter phone number: ")
        if phone:
            record.add(Phone(phone))
        address = input("Enter address: ")
        if address:
            record.set_address(Address(address))
        birthday = input("Please enter birthday (Format: YYYY-MM-DD): ")
        if birthday:
            record.set_birthday(Birthday(birthday))
        email = input("Please enter email:")
        if email:
            record.set_email(Email(email))
        self.address_book.add_record(record)
        return "Contact was added."

    @input_error
    def add(self):
        name = input("Please enter name of person to which you are willing to add info:")
        record = self.address_book.data.get(name)
        if not record:
            return "No such contact - please check your input."
        extra = input("What we are willing to add?(Phone, Address, Birthday, Email):").lower()
        if extra == 'phone':
            phone = input('Please enter extra phone:')
            record.add(Phone(phone))
            return "Phone was added"
        if extra == 'address':
            address = input('Please enter Address:')
            record.set_address(Address(address))
            return "Address was added"
        if extra == 'birthday':
            birthday = input('Please enter Birthday:')
            record.set_birthday(Birthday(birthday))
            return "Birthday was added"
        if extra == 'email':
            email = input('Please enter Email:')
            record.set_email(Email(email))
            return "Email was added"

    @input_error
    def change(self):
        name = input("Please enter name of person:")
        record = self.address_book.data.get(name)
        if not record:
            return "No such contact with phone number."
        phone = input("Enter new phone number: ")
        record.phones = [Phone(phone)]
        return "Result was saved."

    @input_error
    def phone(self):
        name = input("Please enter name of person:")
        record = self.address_book.data.get(name)
        if not record:
            return "No such contact with this phone number."
        return ', '.join([str(phone.value) for phone in record.phones])

    @input_error
    def show(self):
        return "\n".join([str(record.name.value) + ": "
                          + ', '.join([str(phone.value) for phone in record.phones])
                          + (f", Address: {record.address.value}" if record.address else ", [No Address] ")
                          + (f", Email: {record.email.value}" if record.email else ", [No Email] ")
                          + (f", Birthday: {record.birthday.value}" if record.birthday else ", [No Birthday]")
                          for record in self.address_book.get_all_records()])

    @input_error
    def birthday(self):
        name = input("Please enter name of person:")
        record = self.address_book.data.get(name)
        if not record:
            return "No such contact with this name."
        days = record.days_to_birthday()
        if days:
            return f"{days} left till birthday."
        else:
            return "There is no birthday day."

    def search(self):
        query = input("Please enter what we are looking for:")
        for record in self.address_book.values():
            if query.lower() in record.name.value.lower() or any(query in phone.value for phone in record.phones):
                return "\n".join([str(record.name.value) + ": "
                          + ', '.join([str(phone.value) for phone in record.phones])
                          + (f", Address: {record.address.value}" if record.address else ", [No Address] ")
                          + (f", Email: {record.email.value}" if record.email else ", [No Email] ")
                          + (f", Birthday: {record.birthday.value}" if record.birthday else ", [No Birthday]")
                                    for record in self.address_book.get_all_records()])


    @input_error
    def exit(self):
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
                  "Create - Create new Person to Contacts\n"
                  "Add - Add extra info to Contact"
                  "Change {name}- Changing existing phone for contact \n"
                  "Phone {name} - Showing phone for person\n"
                  "Show - Show all contacts in AddressBook\n"
                  "Birthday {name} - How many days till Birthday \n"
                  "Exit - Close Assistant \n")
            while True:
                command = input(">>> ")
                function = getattr(assistant, command.lower(), None)
                if function:
                    print(function())
                else:
                    print("Unknown command - please try one more time.")
                if command == 'exit':
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
