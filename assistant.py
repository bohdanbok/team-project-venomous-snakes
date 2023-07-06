import sys 
from collections import UserDict
from datetime import datetime
import re
import pickle

STOP_WORDS = ['exit', 'good bye', 'close']


class Field:
    def __init__(self, value=None):
        self.value = value
    
    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __repr__(self):
        return f'{self.value}'
    

class Name(Field):
    pass
            

class Phone(Field):
    @Field.value.setter
    def value(self, new_value):
        if not self._is_valid_phone(new_value):
            raise ValueError("Invalid phone number")
        self._value = new_value

    @staticmethod
    def _is_valid_phone(phone):
        phone_regex = r'^\+?3?8?(0\d{9})$'
        if re.search(phone_regex, phone):
            return True
        else:
            raise ValueError('Please write phone number in proper format')


class Birthday(Field):
    @Field.value.setter
    def value(self, new_value):
        if not self._is_valid_birthday(new_value):
            raise ValueError("Invalid birthday")
        self._value = new_value

    @staticmethod
    def _is_valid_birthday(birthday):
        birthday_regex = r'\d{2}-\d{2}-\d{4}'
        if re.search(birthday_regex, birthday):
            return True
        else: 
            raise ValueError('Please write date of birth in format: dd-mm-yyyy')
    

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        if phone:
            self.phones = []
            self.phones.append(Phone(phone))
        if birthday:
            self.birthday = Birthday(birthday)
        
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
        
    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break
            
    def days_to_birthday(self):
        if not hasattr(self, 'birthday') or not self.birthday.value:
            return None

        today = datetime.now().date()
        birthday = datetime.strptime(self.birthday.value, "%d-%m-%Y").date().replace(year=today.year)

        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)

        return (birthday - today).days
    
    def __repr__(self):
        if not hasattr(self, 'birthday') or not self.birthday.value:
            return f'Phones:{self.phones}'
        else:
            return f'Phones:{self.phones}, Birthday:{self.birthday}'
        

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        
    def iterator(self, page_size):
        records = list(self.data.values())
        total_pages = len(records) // page_size + 1

        for page in range(total_pages):
            start = page * page_size
            end = start + page_size
            yield records[start:end]
    
    def save_data(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.data, file)

    def load_data(self, file_path):
        with open(file_path, 'rb') as file:
            self.data = pickle.load(file)

    def search_contacts(self, search_string):
        search_string = search_string.lower()
        matching_contacts = []

        for record in self.data.values():
            if search_string in record.name.value.lower():
                matching_contacts.append(record)
            else:
                for phone in record.phones:
                    if search_string in phone.value.lower():
                        matching_contacts.append(record)
                        break

        return matching_contacts
            

contacts = AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            print("Enter user name")
        except ValueError:
            print("Give me name and phone please")
        except IndexError:
            print("Invalid input. Please try again.")    
    return inner


def greet():
    result = 'How can I help you?'
    return result


def new_contact(user_input):
    parts = user_input.split(" ")
    if len(parts) == 2:
        record = Record(parts[1])
    if len(parts) == 3:
        record = Record(parts[1], parts[2])
    if len(parts) == 4:
        record = Record(parts[1], parts[2], parts[3])
    contacts.add_record(record)   
    result = 'Contact was successfully created'
    return result


def add_phone(user_input):
    parts = user_input.split(" ")
    contacts[parts[1]].add_phone(parts[2])
    result = 'Extra phone was successfully added'
    return result


def remove_contact(user_input):
    parts = user_input.split(" ")
    contacts[parts[1]].remove_phone(parts[2])
    result = 'Phone was removed'
    return result
    

def change_contact(user_input):
    parts = user_input.split(" ")
    contacts[parts[1]].edit_phone(parts[2], parts[3])
    result = 'Contact was successfully updated'
    return result 


def show_contact(user_input):
    parts = user_input.split(" ")
    return contacts[parts[1]]


def show_all():
    return contacts


def days_to_birthday(user_input):
    parts = user_input.split(" ")
    result = str(contacts[parts[1]].days_to_birthday()) + ' days till birthday'
    return result


def search_contacts(user_input):
    parts = user_input.split(" ")
    search_string = ' '.join(parts[1:])
    matching_contacts = contacts.search_contacts(search_string)
    result = ''

    if matching_contacts:
        result += 'Matching contacts:\n'
        for contact in matching_contacts:
            result += str(contact) + '\n'
    else:
        result = 'No matching contacts found'

    return result
        

def process_input(user_input):
    listed_user_input = user_input.split(' ')
    command = listed_user_input[0].lower()
    if command == 'hello':
        return greet()
    elif command == 'create':
        return new_contact(user_input)
    elif command == 'add':
        return add_phone(user_input)
    elif command == 'remove': 
        return remove_contact(user_input)
    elif command == 'change':
        return change_contact(user_input)
    elif command == 'phone': 
        return show_contact(user_input)
    elif command == 'show':
        return show_all()
    elif command == 'when':
        return days_to_birthday(user_input)
    elif command == 'search':
        return search_contacts(user_input)
        

def run_bot():
    while True:
        user_input = input("Write your request: ")
        if user_input not in STOP_WORDS:
            print(process_input(user_input))
        elif user_input in STOP_WORDS:
            filename = input("Enter the filename to save the address book: ")
            contacts.save_data(filename)
            print('Good bye!')
            return sys.exit()


def start():
    filename = input("Enter the filename to load the address book:")
    if len(filename) > 0:
        contacts.load_data(filename)
        print("Address book loaded successfully!")
        run_bot()
    else:
        run_bot()    
        
        
if __name__ == '__main__':        
    start()
    