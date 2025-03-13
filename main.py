import sys
import os

import launcher_ui

import minecraft_launcher_lib
import requests
import shutil
import wget

launcher_version = '1.0.0'


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
    """Возвращает список файлов в указанной папке."""
    return os.listdir(folder_path)


def write_list_to_file(file_list, output_file):
    """Записывает список в текстовый файл построчно."""
    with open(output_file, 'w') as f:
        for item in file_list:
            f.write(f"{item}\n")


def excepthook(exc_type, exc_value, exc_traceback):
    with open("error_report.txt", "a") as f:
        f.write("Unhandled exception occurred:\n")
        import traceback
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)


def main():
    sys.excepthook = excepthook
    # welcome()
    # check_launcher_updates()
    # vanilla_expanded.launch(get_options())
    # file_list = get_file_list("D:\\Python\\JFCRAFT\\download-files\\Middle-Earth-Chronicles-1.7.10\\mods")
    # write_list_to_file(file_list, 'output_file.txt')
    launcher_ui.startup()



if __name__ == '__main__':
    main()
