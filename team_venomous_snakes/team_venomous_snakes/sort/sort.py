import os
import shutil


def sort_files():
    folder_path = input("Please enter path to folder, which you are willing to sort: ")

    if folder_path == "exit":
        print("See you!")

    else:
        try:
            # Створюємо словник категорій файлів
            categories = {
                "зображення": [".jpg", ".jpeg", ".png", ".gif"],
                "документи": [".doc", ".docx", ".txt", ".pdf"],
                "відео": [".mp4", ".avi", ".mov"],
                "інше": []
            }

            # Перебираємо всі файли в папці
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    # Отримуємо розширення файлу
                    extension = os.path.splitext(filename)[1].lower()

                    # Шукаємо відповідну категорію для файлу
                    category = "Other"  # за замовчуванням

                    for key, value in categories.items():
                        if extension in value:
                            category = key
                            break

                    # Створюємо папку категорії, якщо вона ще не існує
                    category_folder = os.path.join(folder_path, category)
                    if not os.path.exists(category_folder):
                        os.makedirs(category_folder)

                    # Переміщуємо файл до відповідної категорії
                    new_file_path = os.path.join(category_folder, filename)
                    shutil.move(file_path, new_file_path)
                    print(f"{filename} Moved to category: {category}")
        except FileNotFoundError:
            print("No such directory - please check it")

            print("Sorting Finished!")


if __name__ == "__main__":
    # Приклад виклику функції для сортування файлів у папці "C:/шлях/до/папки"
    sort_files()
