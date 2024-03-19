import minecraft_launcher_lib
import subprocess
import requests
import os
import shutil


def check_jfcraft(minecraft_directory):
    print('Проверка JFCRAFT...')
    if any(item['id'] == '1.19.2-forge-43.3.5' for item in
           minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)):
        print("JFCRAFT установлен на данном компьютере")
        return True
    else:
        print("JFCRAFT не установлен на данном компьютере")
        return False


def install_jfcraft(minecraft_directory):
    callback = {
        "setStatus": lambda text: print(text, end='\n'),
    }
    print('Начинается установка Forge...')
    minecraft_launcher_lib.forge.install_forge_version('1.19.2-43.3.5', minecraft_directory, callback)
    print('Forge успешно установлен!')


def install_mods(minecraft_directory):
    mods_url = 'https://github.com/jamesfimmer/JFCRAFT-MODS/raw/main/mods.zip'
    mods_folder = minecraft_directory + '\\mods'
    response = requests.get(mods_url)
    with open('mods.zip', 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive('mods.zip', mods_folder, 'zip')
    os.remove('mods.zip')
    print('Моды успешно установлены/обновлены!')


def install_shaderpacks(minecraft_directory):
    shaderpacks_url = 'https://github.com/jamesfimmer/JFCRAFT-MODS/raw/main/options.zip'
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


def launch_jfcraft(minecraft_directory):
    print('Запуск JFCRAFT...')
    subprocess.run(
        minecraft_launcher_lib.command.get_minecraft_command('1.19.2-forge-43.3.5', minecraft_directory,
                                                             get_options()))


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


def main():
    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('.minecraft', '.jfcraft')
    if check_jfcraft(minecraft_directory):
        print('Проверка/обновление модов...')
        install_mods(minecraft_directory)
        launch_jfcraft(minecraft_directory)
    else:
        install_jfcraft(minecraft_directory)
        install_mods(minecraft_directory)
        install_shaderpacks(minecraft_directory)
        install_options(minecraft_directory)
        launch_jfcraft(minecraft_directory)


if __name__ == '__main__':
    main()
