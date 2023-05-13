import random
import string
import pickle

# Имя файла для сохранения истории паролей
HISTORY_FILE = "password_history.pkl"

# Функция просмотра истории паролей и запрос на эту функцию

def view_password_history():
    print("История паролей:")
    for i, password in enumerate(password_history):
        print(f"{i+1}. {password}")

view_history = input("Хотите посмотреть историю паролей? (да/нет): ")
if view_history.lower() == "да":
    view_password_history()

def load_password_history():
    try:
        with open(HISTORY_FILE, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

def save_password_history(password_history):
    with open(HISTORY_FILE, "wb") as f:
        pickle.dump(password_history, f)

# Загружаем историю паролей из файла
password_history = load_password_history()

def generate_password(length, shortened_length=None):
    # Создаем строку, содержащую все символы, которые могут использоваться в пароле
    characters = string.ascii_letters + string.digits + string.punctuation

    # Генерируем пароль из случайных символов
    password = ''.join(random.choice(characters) for i in range(length))

    # Если задана длина скрощенного пароля, скрощаем его
    if shortened_length:
        password = str(hash(password))[-shortened_length:]

    # Добавляем сгенерированный пароль в историю
    password_history.append(password)

    # Сохраняем историю паролей в файл
    save_password_history(password_history)

    return password

# Запрос у пользователя длины пароля и количества генерируемых паролей
password_length = int(input("Введите длину пароля: "))
password_count = int(input("Введите количество генерируемых паролей: "))

# Генерация и вывод паролей с нумерацией
for i in range(password_count):
    password = generate_password(password_length)
    print(f"{i+1}. {password}")

# Запрос у пользователя выбора паролей для слияния
selected_passwords = input("Введите номера паролей через запятую для слияния (например, 1,3,5): ")
selected_passwords = selected_passwords.split(",")
selected_passwords = [int(x.strip()) for x in selected_passwords]

# Слияние выбранных паролей
merged_password = ""
for i in selected_passwords:
    merged_password += password_history[i-1]

# Вывод результата слияния
print(f"Сгенерированный пароль из выбранных: {merged_password}")

# Запрос у пользователя поправок в пароле
password = input("Введите сгенерированный пароль или нажмите Enter, чтобы сгенерировать новый из чифр: ")
if password:
    # Проверяем, есть ли введенный пароль в истории
    if password in password_history:
        print("Этот пароль уже использовался ранее. Пожалуйста, выберите другой.")
    else:
        print("Вы ввели новый пароль:", password)
        # Добавляем новый пароль в историю
        password_history.append(password)
        # Сохраняем историю паролей в файл
        save_password_history(password_history)
else:
    shortened_length = int(input("Введите длину скрощенного пароля или нажмите Enter, чтобы не скращать: "))
    password = generate_password(password_length, shortened_length)
    print("Сгенерированный пароль:", password)
