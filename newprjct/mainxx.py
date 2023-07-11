import re

# Задані команди і відповідні ключові слова
commands = {
    'open_file': ['open', 'open file', 'view'],
    'close_file': ['close', 'close file', 'exit'],
    'search_info': ['find', 'search', 'lookup'],
    'send_message': ['send', 'message', 'deliver']
}

# Функція для визначення найближчої команди
def find_nearest_command(text):
    found_command = None
    max_match = 0

    for command, keywords in commands.items():
        match_count = 0
        for word in keywords:
            if word in text:
                match_count += 1

        if match_count > max_match:
            max_match = match_count
            found_command = command

    return found_command

# Отримання введеного тексту від користувача
input_text = input('Введіть текст: ')

# Виклик функції для пошуку найближчої команди
nearest_command = find_nearest_command(input_text)

# Виведення результату
if nearest_command:
    print('Можлива команда для виконання:', nearest_command)
else:
    print('Команда не знайдена')
