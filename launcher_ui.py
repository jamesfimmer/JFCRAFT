import threading
import tkinter as tk
from tkinter import ttk

import modpack


def launch(version_var, username_entry, min_ram_entry, max_ram_entry, console_output):
    version = version_var.get()
    username = username_entry.get()
    min_ram = min_ram_entry.get()
    max_ram = max_ram_entry.get()

    thread_install = threading.Thread(target=modpack.start_install, args=[version])
    thread_install.start()


def message_to_console(message):
    console_output.insert(tk.END, message)
    console_output.insert(tk.END, '\n')
    console_output.see(tk.END)  # Автоматическая прокрутка до конца


def create_ui():
    # Создание основного окна
    root = tk.Tk()
    root.title("JFCRAFT")
    root.geometry("400x500")  # Устанавливаем размер окна

    # Заголовок
    title_label = tk.Label(root, text="JFCRAFT", font=("Helvetica", 16))
    title_label.pack(pady=10)

    # Пункт выбора версии
    version_label = tk.Label(root, text="Выберите версию:")
    version_label.pack()

    version_var = tk.StringVar()
    version_combobox = ttk.Combobox(root, textvariable=version_var)
    version_combobox['values'] = ("Vanilla Expanded 1.20.1", "Pokecraft 1.20.1")
    version_combobox.current(0)  # Устанавливаем начальное значение
    version_combobox.pack(pady=5)

    # Поле ввода никнейма
    username_label = tk.Label(root, text="Никнейм:")
    username_label.pack()

    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    # Поля ввода для минимальной и максимальной границы ОЗУ
    min_ram_label = tk.Label(root, text="Минимальная граница ОЗУ (MB):")
    min_ram_label.pack()

    min_ram_entry = tk.Entry(root)
    min_ram_entry.pack(pady=5)

    max_ram_label = tk.Label(root, text="Максимальная граница ОЗУ (MB):")
    max_ram_label.pack()

    max_ram_entry = tk.Entry(root)
    max_ram_entry.pack(pady=5)

    # Кнопки "Запустить" и "Установить"
    launch_button = tk.Button(root, text="Запустить",
                              command=lambda: launch(version_var, username_entry, min_ram_entry, max_ram_entry,
                                                     console_output))
    launch_button.pack(pady=10)

    # Окно для вывода сообщений консоли
    global console_output
    console_output = tk.Text(root, height=10, width=50)
    console_output.pack(pady=10)
    console_output.insert(tk.END, "Консоль запущена...\n")

    # Запуск основного цикла обработки событий
    root.mainloop()


def startup():
    thread_ui = threading.Thread(target=create_ui())
    thread_ui.start()


if __name__ == "__main__":
    create_ui()
