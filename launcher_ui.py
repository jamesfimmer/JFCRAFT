import json
import os
import threading
import tkinter as tk
from tkinter import ttk

import modpack

launcher_version = '1.1.0'
config_file = 'launcher_config.json'


def launch(version_var, username_entry, min_ram_entry, max_ram_entry):
    version = version_var.get()
    username = username_entry.get()
    min_ram = min_ram_entry.get()
    max_ram = max_ram_entry.get()
    jvmArguments = [f'-Xms{min_ram}G', f'-Xmx{max_ram}G']
    save_config(username, min_ram, max_ram, version)

    thread_install = threading.Thread(target=modpack.launch, args=[version, username, jvmArguments, launcher_version])
    thread_install.start()


def message_to_console(message):
    console_output.insert(tk.END, message)
    console_output.insert(tk.END, '\n')
    console_output.see(tk.END)


def load_config():
    if os.path.exists(config_file):  # Проверяем, существует ли файл
        with open(config_file, 'r') as f:
            return json.load(f)  # Загружаем настройки из JSON
    # Если файла нет, создаём стандартные значения
    return {"username": "", "min_ram": "2", "max_ram": "5", "version": "PokeCraft 1.20.1"}


def save_config(username, min_ram, max_ram, version):
    data = {
        "username": username,
        "min_ram": min_ram,
        "max_ram": max_ram,
        "version": version
    }
    with open(config_file, 'w') as f:
        json.dump(data, f)  # Записываем в JSON


def create_ui():
    root = tk.Tk()
    root.title("JFCRAFT")
    root.geometry("400x550")

    # Загружаем сохранённые настройки
    config = load_config()

    title_label = tk.Label(root, text="JFCRAFT", font=("Helvetica", 16))
    title_label.pack(pady=5)

    version_label = tk.Label(root, text=f'Текущая версия лаунчера: {launcher_version}', font=("Helvetica", 8))
    version_label.pack(pady=5)

    # Выбор версии
    version_var = tk.StringVar(value=config['version'])
    version_combobox = ttk.Combobox(root, textvariable=version_var)
    version_combobox['values'] = (
        "PokeCraft 1.20.1", "Vanilla Expanded 1.20.1", "WinterCraft 1.20.1", "Middle-Earth Chronicles 1.7.10")
    version_combobox.pack(pady=5)

    # Поле имени пользователя
    username_label = tk.Label(root, text="Имя пользователя:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.insert(0, config['username'])  # Подставляем имя из сохранённых данных
    username_entry.pack(pady=5)

    # Поле минимального RAM
    min_ram_label = tk.Label(root, text="Минимальная граница ОЗУ в ГБ:")
    min_ram_label.pack()
    min_ram_entry = tk.Entry(root)
    min_ram_entry.insert(0, config['min_ram'])  # Подставляем min RAM
    min_ram_entry.pack(pady=5)

    # Поле максимального RAM
    max_ram_label = tk.Label(root, text="Максимальная граница ОЗУ в ГБ:")
    max_ram_label.pack()
    max_ram_entry = tk.Entry(root)
    max_ram_entry.insert(0, config['max_ram'])  # Подставляем max RAM
    max_ram_entry.pack(pady=5)

    # Кнопка "Запустить"
    launch_button = tk.Button(root, text="Запустить",
                              command=lambda: launch(version_var, username_entry, min_ram_entry, max_ram_entry))
    launch_button.pack(pady=5)

    # Консольный вывод
    global console_output
    console_output = tk.Text(root, height=10, width=50)
    console_output.pack(pady=10)
    console_output.insert(tk.END, "Консоль запущена...\n")

    root.mainloop()


def startup():
    thread_ui = threading.Thread(target=create_ui())
    thread_ui.start()


if __name__ == "__main__":
    create_ui()
