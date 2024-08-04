import os

import requests
from requests import HTTPError, Timeout, RequestException

import launcher_ui

import minecraft_launcher_lib

modpack = ''
forge_version_for_install = ''
forge_version_for_check = ''
minecraft_directory = ''
mods_directory = ''
shaderpacks_directory = ''

url = ''
mods_list_url = ''
shaderpacks_url = ''
config_url = ''


def check_for_installed_forge():
    launcher_ui.message_to_console(f'Проверка Forge для {modpack}...')
    print(forge_version_for_check)
    if any(item['id'] == forge_version_for_check for item in
           minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)):
        launcher_ui.message_to_console(f"Forge для {modpack} установлен на данном компьютере!")
    else:
        launcher_ui.message_to_console(f"Forge для {modpack} не установлен на данном компьютере!")
        install_forge()


def install_forge():
    launcher_ui.message_to_console(f'Начало установки Forge для {modpack}')
    callback = {
        "setStatus": lambda text: launcher_ui.message_to_console(text),
    }
    minecraft_launcher_lib.forge.install_forge_version(forge_version_for_install, minecraft_directory, callback)
    print(f'Forge для {modpack} успешно установлен!')


def get_installed_mods():
    if not os.path.exists(mods_directory):
        os.makedirs(mods_directory)

    try:
        return os.listdir(mods_directory)
    except FileNotFoundError:
        launcher_ui.message_to_console('Папка mods не была обнаружена')
        return []
    except NotADirectoryError:
        return []


def check_for_installed_mods():
    installed_mods_list = get_installed_mods()
    launcher_ui.message_to_console('Установленные моды: ')
    launcher_ui.message_to_console(installed_mods_list)
    actual_mods_list = requests.get(mods_list_url, verify=False).text.splitlines()
    launcher_ui.message_to_console('Актуальные моды: ')
    launcher_ui.message_to_console(actual_mods_list)

    delete_extra_mods(installed_mods_list, actual_mods_list)
    install_mods(installed_mods_list, actual_mods_list)

    pass


def delete_extra_mods(installed_mods_list, actual_mods_list):
    mods_to_remove = [mod for mod in installed_mods_list if mod not in actual_mods_list]
    if mods_to_remove:
        launcher_ui.message_to_console('Обнаружены лишние моды!!!')
        launcher_ui.message_to_console('Моды для удаления: ')
        launcher_ui.message_to_console(mods_to_remove)
        for mod in mods_to_remove:
            os.remove(mods_directory + '\\' + mod)
            launcher_ui.message_to_console('Успешно удалён лишний мод: ' + mod)
    else:
        launcher_ui.message_to_console('Лишних модов не обнаружено')
        return


def install_mods(installed_mods_list, actual_mods_list):
    mods_to_install = [mod for mod in actual_mods_list if mod not in installed_mods_list]
    if mods_to_install:
        launcher_ui.message_to_console('Начало установки модификаций...')
        launcher_ui.message_to_console('Моды для установки: ')
        print(mods_to_install)
        for mod in mods_to_install:
            download_file(url + 'mods/' + mod, mods_directory, mod)

            launcher_ui.message_to_console('\nУспешно загружен мод: ' + mod)
            launcher_ui.message_to_console('По пути: ' + mods_directory + '\\' + mod)
    else:
        print('Все модификации на месте!!!')
        return


def download_file(url, local_path, name):
    try:
        # Отправляем GET запрос для получения файла
        with requests.get(url, stream=True) as response:
            # Проверяем, успешен ли запрос
            response.raise_for_status()

            # Открываем локальный файл для записи
            with open(mods_directory + '\\' + name, 'wb') as file:
                # Записываем содержимое файла по частям (чтобы избежать больших загрузок в память)
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def set_global_variables(version):
    global modpack, forge_version_for_install, forge_version_for_check, minecraft_directory, mods_directory, shaderpacks_directory, url, mods_list_url
    if version == 'Vanilla Expanded 1.20.1':
        modpack = 'Vanilla Expanded 1.20.1'
        forge_version_for_install = '1.20.1-47.2.0'
        forge_version_for_check = '1.20.1-forge-47.2.0'
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('.minecraft',
                                                                                             '.jfcraft-Vanilla-Expanded-1.20.1')
        mods_directory = minecraft_directory + '\\mods'
        shaderpacks_directory = minecraft_directory + '\\shaderpacks'

        url = 'https://github.com/jamesfimmer/JFCRAFT/raw/main/download-files/VanillaExpanded-1.20.1/'
        mods_list_url = url + 'mod_list.txt'
    elif version == 'Pokecraft 1.20.1':
        modpack = 'Pokecraft 1.20.1'
        forge_version_for_install = '1.20.1-47.3.0'
        forge_version_for_check = '1.20.1-forge-47.3.0'
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('.minecraft',
                                                                                             '.jfcraft-Pokecraft-1.20.1')
        mods_directory = minecraft_directory + '\\mods'
        shaderpacks_directory = minecraft_directory + '\\shaderpacks'
        url = 'https://github.com/jamesfimmer/JFCRAFT/raw/main/download-files/Pokecraft-1.20.1/'
        mods_list_url = url + 'mod_list.txt'


def start_install(version):
    set_global_variables(version)
    check_for_installed_forge()
    check_for_installed_mods()


if __name__ == '__main__':
    start_install()
