import os
import shutil
import subprocess
import minecraft_launcher_lib
import requests
import wget

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('.minecraft',
                                                                                     '.jfcraft-Vanilla-Expanded-1.20.1')
mods_directory = minecraft_directory + '\\mods'
shaderpacks_directory = minecraft_directory + '\\shaderpacks'
actual_mods_list_url = 'https://github.com/jamesfimmer/jfcraft-download-files/raw/main/VanillaExpanded-1.20.1/mod_list.txt'


def check_for_installed_forge():
    print('Проверка Forge для Vanilla-Expanded-1.20.1...')
    if any(item['id'] == '1.20.1-forge-47.2.0' for item in
           minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)):
        print("Forge для Vanilla-Expanded-1.20.1... установлен на данном компьютере")
        check_for_installed_mods()
        return True
    else:
        print("Forge для Vanilla-Expanded-1.20.1 не установлен на данном компьютере")
        install_forge()
        check_for_installed_mods()
        return False


def install_forge():
    print('Начало установки Forge для Vanilla-Expanded-1.20.1...')
    callback = {
        "setStatus": lambda text: print(text, end='\n'),
    }
    minecraft_launcher_lib.forge.install_forge_version('1.20.1-47.2.0', minecraft_directory, callback)
    print('Forge для Vanilla-Expanded-1.20.1 успешно установлен!')


def get_installed_mods():
    try:
        return os.listdir(mods_directory)
    except FileNotFoundError:
        print('Папка mods не была обнаружена')
        return []


def check_for_installed_mods():
    installed_mods_list = get_installed_mods()
    print('Установленные моды: ')
    print(installed_mods_list)
    actual_mods_list = requests.get(actual_mods_list_url).text.splitlines()
    print('Актуальные моды: ')
    print(actual_mods_list)

    delete_extra_mods(installed_mods_list, actual_mods_list)
    install_mods(installed_mods_list, actual_mods_list)

    pass


def delete_extra_mods(installed_mods_list, actual_mods_list):
    mods_to_remove = [mod for mod in installed_mods_list if mod not in actual_mods_list]
    if mods_to_remove:
        print('Обнаружены лишние моды!!!')
        print('Моды для удаления: ')
        print(mods_to_remove)
        for mod in mods_to_remove:
            os.remove(mods_directory + '\\' + mod)
            print('Успешно удалён лишний мод: ' + mod)
    else:
        print('Лишних модов не обнаружено')
        return


def install_mods(installed_mods_list, actual_mods_list):
    mods_to_install = [mod for mod in actual_mods_list if mod not in installed_mods_list]
    if mods_to_install:
        print('Начало установки модификаций...')
        print('Моды для установки: ')
        print(mods_to_install)
        for mod in mods_to_install:
            wget.download(
                'https://github.com/jamesfimmer/jfcraft-download-files/raw/main/VanillaExpanded-1.20.1/mods/' + mod,
                mods_directory)
            print('Успешно загружен мод: ' + mod)
    else:
        print('Все модификации на месте!!!')
        return


def check_for_installed_shaderpacks():
    pass


def install_shaderpacks():
    shaderpacks_url = 'https://github.com/jamesfimmer/JFCRAFT-MODS/raw/main/shaderpacks.zip'
    response = requests.get(shaderpacks_url)
    with open('shaderpacks.zip', 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive('shaderpacks.zip', shaderpacks_directory, 'zip')
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
    print('Запуск Vanilla Expanded...')
    subprocess.run(
        minecraft_launcher_lib.command.get_minecraft_command('1.20.1-forge-47.2.0', minecraft_directory,
                                                             options))