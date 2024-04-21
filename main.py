import minecraft_launcher_lib
import subprocess
import requests
import os
import shutil
import wget

launcher_version = '1.0.0'
minecraft_directory_new_ic = minecraft_launcher_lib.utils.get_minecraft_directory().replace('.minecraft',
                                                                                            '.jfcraft-NewIc-1.19.2')
minecraft_directory_vanilla_expanded = minecraft_launcher_lib.utils.get_minecraft_directory().replace('.minecraft',
                                                                                                      '.jfcraft-Vanilla-Expanded-1.20.1')
vanilla_expanded_mods_url = 'https://github.com/jamesfimmer/jfcraft-download-files/raw/main/VanillaExpended-1.20.1/mods.rar'

new_ic_mods_url = 'https://github.com/jamesfimmer/jfcraft-download-files/raw/main/NewIC-1.19.2/mods.zip'


def check_jfcraft_new_ic(minecraft_directory):
    print('Проверка сборки NewIC-1.19.2...')
    if any(item['id'] == '1.19.2-forge-43.3.5' for item in
           minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)):
        print("NewIC-1.19.2 установлен на данном компьютере")
        return True
    else:
        print("NewIC-1.19.2 не установлен на данном компьютере")
        return False


def check_jfcraft_vanilla_expanded(minecraft_directory):
    print('Проверка JFCRAFT Vanilla Expanded')
    if any(item['id'] == '1.20.1-forge-47.2.0' for item in
           minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)):
        print("Vanilla-Expended-1.20.1 установлен на данном компьютере")
        return True
    else:
        print("Vanilla-Expended-1.20.1 не установлен на данном компьютере")
        return False


def install_forge_jfcraft_new_ic(minecraft_directory):
    callback = {
        "setStatus": lambda text: print(text, end='\n'),
    }
    print('Начинается установка Forge...')
    minecraft_launcher_lib.forge.install_forge_version('1.19.2-43.3.5', minecraft_directory, callback)
    print('Forge успешно установлен!')


def install_forge_jfcraft_vanilla_expanded(minecraft_directory):
    callback = {
        "setStatus": lambda text: print(text, end='\n'),
    }
    print('Начинается установка Forge...')
    minecraft_launcher_lib.forge.install_forge_version('1.20.1-47.2.0', minecraft_directory, callback)
    print('Forge успешно установлен!')


def install_mods_jfcraft_new_ic(minecraft_directory):
    mods_folder = minecraft_directory + '\\mods'
    response = requests.get(new_ic_mods_url)
    with open('mods.zip', 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive('mods.zip', mods_folder, 'zip')
    os.remove('mods.zip')
    print('Моды успешно установлены/обновлены!')


def install_mods_jfcraft_vanilla_expanded(minecraft_directory):
    mods_folder = minecraft_directory + '\\mods'
    response = requests.get(vanilla_expanded_mods_url)
    with open('mods.zip', 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive('mods.zip', mods_folder, 'zip')
    os.remove('mods.zip')
    print('Моды успешно установлены/обновлены!')


def install_shaderpacks(minecraft_directory):
    shaderpacks_url = 'https://github.com/jamesfimmer/JFCRAFT-MODS/raw/main/shaderpacks.zip'
    shaderpacks_folder = minecraft_directory + '\\shaderpacks'
    response = requests.get(shaderpacks_url)
    with open('shaderpacks.zip', 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive('shaderpacks.zip', shaderpacks_folder, 'zip')
    os.remove('shaderpacks.zip')
    print('Шейдеры успешно установлены!')


def install_options(minecraft_directory):
    options_url = 'https://github.com/jamesfimmer/JFCRAFT-MODS/raw/main/options.zip'
    options_folder = minecraft_directory
    response = requests.get(options_url)
    with open('options.zip', 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive('options.zip', options_folder, 'zip')
    os.remove('options.zip')
    print('Профиль настроек успешно загружен!')


def launch_jfcraft_new_ic(minecraft_directory, options):
    print('Запуск NewIC...')
    subprocess.run(
        minecraft_launcher_lib.command.get_minecraft_command('1.19.2-forge-43.3.5', minecraft_directory,
                                                             options))


def launch_jfcraft_vanilla_expanded(minecraft_directory, options):
    print('Запуск Vanilla Expanded...')
    subprocess.run(
        minecraft_launcher_lib.command.get_minecraft_command('1.20.1-forge-47.2.0', minecraft_directory,
                                                             options))


def get_username():
    username = input('Пожалуйста введите ваш никнейм: ')
    return username


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


def main():
    welcome()
    check_jfcraft_new_ic(minecraft_directory_new_ic)
    check_jfcraft_vanilla_expanded(minecraft_directory_vanilla_expanded)
    launch_jfcraft_new_ic(minecraft_directory_new_ic, get_options())
    # install_forge_jfcraft_new_ic(minecraft_directory_new_ic)
    # install_forge_jfcraft_vanilla_expanded(minecraft_directory_vanilla_expanded)
    # check_for_update(minecraft_directory)
    # if check_jfcraft(minecraft_directory):
    #     print('Проверка/обновление модов...')
    #     install_mods(minecraft_directory)
    #     launch_jfcraft(minecraft_directory, get_options())
    # else:
    #     install_jfcraft(minecraft_directory)
    #     install_mods(minecraft_directory)
    #     install_shaderpacks(minecraft_directory)
    #     install_options(minecraft_directory)
    #     launch_jfcraft(minecraft_directory, get_options())


if __name__ == '__main__':
    main()
