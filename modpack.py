import os
import subprocess

import rarfile
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
resourcepacks_directory = ''

url = ''
mods_list_url = ''
shaderpacks_url = ''
resourcepacks_url = ''
options_url = ''
servers_url = ''
config_url = ''


def check_for_installed_forge():
    launcher_ui.message_to_console(f'Проверка Forge для {modpack}...')
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
    launcher_ui.message_to_console(f'Forge для {modpack} успешно установлен!')


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
    launcher_ui.message_to_console('Проверка модов...')
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
        launcher_ui.message_to_console('Обнаружены лишние моды!')
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
        launcher_ui.message_to_console(mods_to_install)
        for mod in mods_to_install:
            download_file(url + 'mods/' + mod, mods_directory, mod)

            launcher_ui.message_to_console('\nУспешно загружен мод: ' + mod)
            launcher_ui.message_to_console('По пути: ' + mods_directory + '\\' + mod)
    else:
        launcher_ui.message_to_console('Все модификации на месте!!!')
        return


def check_for_installed_shaderpacks():
    try:
        if os.listdir(shaderpacks_directory):
            launcher_ui.message_to_console('Шейдеры обнаружены!')
            return
        else:
            install_shaderpacks()

    except FileNotFoundError:
        launcher_ui.message_to_console('Папка shaderpacks не была обнаружена')
        install_shaderpacks()

    except NotADirectoryError:
        launcher_ui.message_to_console('Папка shaderpacks не была обнаружена')
        install_shaderpacks()


def install_shaderpacks():
    download_file(shaderpacks_url, minecraft_directory, 'shaderpacks.rar')
    extract_rar(minecraft_directory + '\\shaderpacks.rar', minecraft_directory)

    launcher_ui.message_to_console("Установка ресурс паков")
    download_file(resourcepacks_url, minecraft_directory, 'resourcepacks.rar')
    extract_rar(minecraft_directory + '\\resourcepacks.rar', minecraft_directory)
    launcher_ui.message_to_console('Шейдеры успешно установлены!')


def check_for_installed_options_files():
    if not os.path.exists(minecraft_directory + '\\' + 'options.txt'):
        launcher_ui.message_to_console('Не обнаружен options.txt !!!')
        launcher_ui.message_to_console('Загрузка options.txt...')
        download_file(options_url, minecraft_directory, 'options.txt')
    if not os.path.exists(minecraft_directory + '\\' + 'servers.dat'):
        launcher_ui.message_to_console('Не обнаружен servers.dat !!!')
        launcher_ui.message_to_console('Загрузка servers.dat...')
        download_file(options_url, minecraft_directory, 'servers.dat')
    if not os.path.exists(minecraft_directory + '\\' + 'config'):
        launcher_ui.message_to_console('Не обнаружена папка config !!!')
        launcher_ui.message_to_console('Загрузка config...')
        download_file(config_url, minecraft_directory, 'config.rar')
        extract_rar(minecraft_directory + '\\config.rar', minecraft_directory)
        launcher_ui.message_to_console('Конфиги успешно установлены!')


def extract_rar(rar_path, extract_to):
    try:
        # Создаем директорию, если она не существует
        os.makedirs(extract_to, exist_ok=True)

        # Распаковываем архив
        with rarfile.RarFile(rar_path) as rf:
            rf.extractall(extract_to)
    except rarfile.BadRarFile as rar_err:
        print(f"Rar file error: {rar_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def download_file(url, local_path, name):
    try:
        # Отправляем GET запрос для получения файла
        with requests.get(url, stream=True) as response:
            # Проверяем, успешен ли запрос
            response.raise_for_status()

            # Открываем локальный файл для записи
            with open(local_path + '\\' + name, 'wb') as file:
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
    global modpack, forge_version_for_install, forge_version_for_check, minecraft_directory, mods_directory, shaderpacks_directory, resourcepacks_directory, url, mods_list_url, \
        shaderpacks_url, resourcepacks_url, options_url, servers_url, config_url
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
        shaderpacks_url = url + 'shaderpacks.rar'
        options_url = url + 'options.txt'
        servers_url = url + 'servers.dat'
        config_url = url + 'config.rar'
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
        shaderpacks_url = url + 'shaderpacks.rar'
        options_url = url + 'options.txt'
        servers_url = url + 'servers.dat'
        config_url = url + 'config.rar'
    elif version == 'WinterCraft 1.20.1':
        modpack = 'WinterCraft 1.20.1'
        forge_version_for_install = '1.20.1-47.3.0'
        forge_version_for_check = '1.20.1-forge-47.3.0'
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('.minecraft',
                                                                                             '.jfcraft-WinterCraft-1.20.1')
        mods_directory = minecraft_directory + '\\mods'
        shaderpacks_directory = minecraft_directory + '\\shaderpacks'
        resourcepacks_directory = minecraft_directory + '\\resourcepacks'
        url = 'https://github.com/jamesfimmer/JFCRAFT/raw/main/download-files/WinterCraft-1.20.1/'
        mods_list_url = url + 'mod_list.txt'
        shaderpacks_url = url + 'shaderpacks.rar'
        resourcepacks_url = url + 'resourcepacks.rar'
        options_url = url + 'options.txt'
        servers_url = url + 'servers.dat'
        config_url = url + 'config.rar'
    elif version == 'Middle-Earth Chronicles 1.7.10':
        modpack = 'Middle-Earth Chronicles 1.7.10'
        forge_version_for_install = '1.7.10-10.13.4.1614-1.7.10'
        forge_version_for_check = 'Forge 10.13.4.1614-1.7.10'
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('.minecraft',
                                                                                             '.jfcraft-Middle-Earth-Chronicles-1.7.10')
        mods_directory = minecraft_directory + '\\mods'
        shaderpacks_directory = minecraft_directory + '\\shaderpacks'
        resourcepacks_directory = minecraft_directory + '\\resourcepacks'
        url = 'https://github.com/jamesfimmer/JFCRAFT/raw/main/download-files/Middle-Earth-Chronicles-1.7.10/'
        mods_list_url = url + 'mod_list.txt'
        shaderpacks_url = url + 'shaderpacks.rar'
        resourcepacks_url = url + 'resourcepacks.rar'
        options_url = url + 'options.txt'
        servers_url = url + 'servers.dat'
        config_url = url + 'config.rar'


def get_ip():
    current_ip = requests.get(
        'https://github.com/jamesfimmer/JFCRAFT/raw/main/download-files/launcher/curreint_ip.txt', verify=False)
    return current_ip.text


def get_port():
    current_port = requests.get(
        'https://github.com/jamesfimmer/JFCRAFT/raw/main/download-files/launcher/current_port.txt', verify=False)
    return current_port.text


def get_options(username, jvmArguments, launcher_version):
    options = {
        'username': username,
        'launcherName': 'JFCRAFT',
        'launcherVersion': launcher_version,
        'server': get_ip(),
        'port': get_port(),
        'jvmArguments': jvmArguments
    }
    return options


def launch(version, username, jvmArguments, launcher_version):
    set_global_variables(version)
    check_for_installed_forge()
    check_for_installed_mods()
    check_for_installed_shaderpacks()
    check_for_installed_options_files()
    launcher_ui.message_to_console(f'Запуск {modpack}...')

    subprocess.run(
            minecraft_launcher_lib.command.get_minecraft_command(forge_version_for_check, minecraft_directory,
                                                             get_options(username, jvmArguments, launcher_version)))


if __name__ == '__main__':
    launch()
