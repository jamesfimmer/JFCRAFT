import minecraft_launcher_lib
import subprocess
import requests
import os
import shutil
import wget
import new_ic
import vanilla_expanded

launcher_version = '1.0.0'


def get_username():
    username = input('Пожалуйста введите ваш никнейм: ')
    return username


def get_ip():
    
    pass


def get_options():
    options = {
        'username': get_username(),
        'launcherName': 'JFCRAFT',
        'launcherVersion': '0.0.1',
        'server': '5.165.58.207',
        'port': '25565'
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


def check_for_update(minecraft_directory):
    print('Проверка обновлений лаунчера...')
    launcher_version_url = \
        'https://github.com/jamesfimmer/jfcraft-download-files/raw/main/jfcraft-launcher/current_version.txt'
    resp = requests.get(launcher_version_url)
    if resp.status_code == 200:
        if resp.text == launcher_version:
            print('Установлена новейшая версия!')
        else:
            print(f'Доступна новая версия {resp.text}...начало установки...')
            download_newest_launcher_version(minecraft_directory)
    else:
        print(f'Ошибка при загрузке актуальной версии, код {resp.status_code}')


def download_newest_launcher_version(minecraft_directory):
    launcher_exe_url = 'https://github.com/jamesfimmer/jfcraft-download-files/raw/main/jfcraft-launcher/JFCRAFT.exe'
    launcher_exe_folder_path = minecraft_directory + '\\JFCRAFT'
    resp = requests.get(launcher_exe_url)

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


def main():
    welcome()
    vanilla_expanded.check_for_installed_forge()


if __name__ == '__main__':
    main()
