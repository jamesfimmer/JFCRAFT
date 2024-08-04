import os
import shutil
import subprocess

import minecraft_launcher_lib
import requests

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('.minecraft',
                                                                                     'jfcraft-NewIc-1.19.2')
mods_url = 'https://github.com/jamesfimmer/jfcraft-download-files/raw/main/NewIC-1.19.2/mods.zip'


def check_for_installed_forge():
    print('Проверка сборки NewIC-1.19.2...')
    if any(item['id'] == '1.19.2-forge-43.3.5' for item in
           minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)):
        print("NewIC-1.19.2 установлен на данном компьютере")
        return True
    else:
        print("NewIC-1.19.2 не установлен на данном компьютере")
        return False


def install_forge():
    callback = {
        "setStatus": lambda text: print(text, end='\n'),
    }
    print('Начинается установка Forge...')
    minecraft_launcher_lib.forge.install_forge_version('1.19.2-43.3.5', minecraft_directory, callback)
    print('Forge успешно установлен!')


def check_for_installed_mods():
    pass


def install_mods():
    mods_folder = minecraft_directory + '\\mods'
    response = requests.get(mods_url)
    with open('mods.zip', 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive('mods.zip', mods_folder, 'zip')
    os.remove('mods.zip')
    print('Моды успешно установлены/обновлены!')


def check_for_installed_shaderpacks():
    pass


def install_shaderpacks():
    shaderpacks_url = 'https://github.com/jamesfimmer/JFCRAFT-MODS/raw/main/shaderpacks.zip'
    shaderpacks_folder = minecraft_directory + '\\shaderpacks'
    response = requests.get(shaderpacks_url)
    with open('shaderpacks.zip', 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive('shaderpacks.zip', shaderpacks_folder, 'zip')
    os.remove('shaderpacks.zip')
    print('Шейдеры успешно установлены!')


def install_options():
    options_url = 'https://github.com/jamesfimmer/JFCRAFT-MODS/raw/main/options.zip'
    options_folder = minecraft_directory
    response = requests.get(options_url)
    with open('options.zip', 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive('options.zip', options_folder, 'zip')
    os.remove('options.zip')
    print('Профиль настроек успешно загружен!')


def launch(options):
    print('Запуск NewIC...')
    subprocess.run(
        minecraft_launcher_lib.command.get_minecraft_command('1.19.2-forge-43.3.5', minecraft_directory,
                                                             options))
