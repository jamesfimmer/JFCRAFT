import sys
import os
import subprocess

import new_ic
import vanilla_expanded
import launcher_ui

import minecraft_launcher_lib
import requests
import shutil
import wget

launcher_version = '1.0.0'


def get_username():
    username = input('Пожалуйста введите ваш никнейм: ')
    return username


def get_ip():
    current_ip = requests.get(
        'https://github.com/jamesfimmer/JFCRAFT/raw/main/download-files/launcher/curreint_ip.txt', verify=False)
    return current_ip.text


def get_port():
    current_port = requests.get(
        'https://github.com/jamesfimmer/JFCRAFT/raw/main/download-files/launcher/current_port.txt', verify=False)
    return current_port.text


def get_jvmArguments():
    xms = input(
        'Пожалуйста введите количество оперативной памяти в гигабайтах для минимального порога (оптимально 2-3): ')
    xmx = input(
        'Пожалуйста введите количество оперативной памяти в гигабайтах для максимального порога (оптимально 6-8): ')
    return [f'-Xms{xms}G', f'-Xmx{xmx}G']


def get_options():
    options = {
        'username': get_username(),
        'launcherName': 'JFCRAFT',
        'launcherVersion': launcher_version,
        'server': get_ip(),
        'port': get_port(),
        'jvmArguments': get_jvmArguments()
    }
    return options


def welcome():
    print('''
    ░░░░░██╗███████╗░█████╗░██████╗░░█████╗░███████╗████████╗
    ░░░░░██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
    ░░░░░██║█████╗░░██║░░╚═╝██████╔╝███████║█████╗░░░░░██║░░░
    ██╗░░██║██╔══╝░░██║░░██╗██╔══██╗██╔══██║██╔══╝░░░░░██║░░░
    ╚█████╔╝██║░░░░░╚█████╔╝██║░░██║██║░░██║██║░░░░░░░░██║░░░
    ░╚════╝░╚═╝░░░░░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░░░░╚═╝░░░''')
    print('Приветствую! Спасибо за использование моего лаунчера. По всем вопросам в Telegram @jamesfimmer')
    print(f'Версия лаунчера: {launcher_version}')


def check_launcher_updates():
    print('Проверка обновлений лаунчера...')
    resp = requests.get('https://github.com/jamesfimmer/JFCRAFT/raw/main/download-files/launcher/current_version.txt',
                        verify=False)
    if resp.status_code == 200:
        if resp.text == launcher_version:
            print('Установлена новейшая версия!')
        else:
            print(f'Доступна новая версия {resp.text}...начало установки...')
            download_newest_launcher_version()
    else:
        print(f'Ошибка при загрузке актуальной версии, код {resp.status_code}')


def download_newest_launcher_version():
    launcher_exe_url = 'https://github.com/jamesfimmer/JFCRAFT/raw/main/download-files/launcher/JFCRAFT.exe'
    launcher_exe_folder_path = minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace(
        '.minecraft',
        '.JFCRAFT')
    resp = requests.get(launcher_exe_url, verify=False)

    if os.path.exists(launcher_exe_folder_path):
        try:
            shutil.rmtree(launcher_exe_folder_path)
        except OSError as e:
            print(f'Ошибка при очищении папки: {e}')
    try:
        os.makedirs(launcher_exe_folder_path)
        print(f'Папка успешно создана.')
    except OSError as error:
        print(f'Ошибка при создании папки: {error}')

    wget.download(launcher_exe_url, launcher_exe_folder_path)
    print(f'Успешно загружена новая версия лаунчера! Её можно найти по пути {launcher_exe_folder_path}\JFCRAFT.exe')
    print('Текущее окно можно закрыть и удалить старый .exe файл!')
    exit()


def get_file_list(folder_path):
    return os.listdir(folder_path)


def excepthook(exc_type, exc_value, exc_traceback):
    with open("error_report.txt", "a") as f:
        f.write("Unhandled exception occurred:\n")
        import traceback
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)


def list_files_in_directory(directory_path, output_file):
    try:
        # Получаем список всех файлов и папок в указанной директории
        files_and_folders = os.listdir(directory_path)

        # Оставляем только файлы
        files = [f for f in files_and_folders if os.path.isfile(os.path.join(directory_path, f))]

        # Записываем имена файлов в текстовый файл
        with open(output_file, 'w') as file:
            for file_name in files:
                file.write(file_name + '\n')

        print(f"Список файлов успешно записан в '{output_file}'")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def main():
    sys.excepthook = excepthook
    # welcome()
    # check_launcher_updates()
    # vanilla_expanded.launch(get_options())
    print(os.listdir('C:\\Users\\James\\AppData\\Roaming\\.minecraft\\versions\\Pokecraft 1.20.1\\mods'))
    list_files_in_directory('C:\\Users\\James\\AppData\\Roaming\\.minecraft\\versions\\Pokecraft 1.20.1\\mods', 'mod_list.txt')
    launcher_ui.startup()


if __name__ == '__main__':
    main()
