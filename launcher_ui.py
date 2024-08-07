import threading
import tkinter as tk
from tkinter import ttk

import modpack

launcher_version = '1.1.0'


def launch(version_var, username_entry, min_ram_entry, max_ram_entry):
    version = version_var.get()
    username = username_entry.get()
    min_ram = min_ram_entry.get()
    max_ram = max_ram_entry.get()
    jvmArguments = [f'-Xms{min_ram}G', f'-Xmx{max_ram}G']

    thread_install = threading.Thread(target=modpack.launch, args=[version, username, jvmArguments, launcher_version])
    thread_install.start()


def message_to_console(message):
    console_output.insert(tk.END, message)
    console_output.insert(tk.END, '\n')
    console_output.see(tk.END)


def create_ui():
    root = tk.Tk()
    root.title("JFCRAFT")
    root.geometry("400x500")


    title_label = tk.Label(root, text="JFCRAFT", font=("Helvetica", 16))
    title_label.pack(pady=0)

    title_label = tk.Label(root, text='Текущая версия лаунчера: ' + launcher_version, font=("Helvetica", 8))
    title_label.pack(pady=10)
    version_label = tk.Label(root, text="Выберите версию:")
    version_label.pack()

    version_var = tk.StringVar()
    version_combobox = ttk.Combobox(root, textvariable=version_var)
    version_combobox['values'] = ("Pokecraft 1.20.1", "Vanilla Expanded 1.20.1")
    version_combobox.current(0)
    version_combobox.pack(pady=5)

    username_label = tk.Label(root, text="Имя пользователя:")
    username_label.pack()

    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    min_ram_label = tk.Label(root, text="Минимальная граница ОЗУ в гигабайтах (рекомендуется 2-3):")
    min_ram_label.pack()

    min_ram_entry = tk.Entry(root)
    min_ram_entry.pack(pady=5)

    max_ram_label = tk.Label(root, text="Максимальная граница ОЗУ в гигабайтах (рекомендуется 5-6):")
    max_ram_label.pack()

    max_ram_entry = tk.Entry(root)
    max_ram_entry.pack(pady=5)

    launch_button = tk.Button(root, text="Запустить",
                              command=lambda: launch(version_var, username_entry, min_ram_entry, max_ram_entry,))
    launch_button.pack(pady=10)

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
