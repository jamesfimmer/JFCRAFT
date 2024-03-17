import minecraft_launcher_lib
import subprocess
import requests
import os
from zipfile import ZipFile
import shutil

def main():
    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('.minecraft', '.jfcraft')
    callback = {
        "setStatus": lambda text: print(text, end='\n'),
    }
    print("Установка сборки ...")
    #minecraft_launcher_lib.forge.install_forge_version('1.19.2-43.3.5', minecraft_directory, callback)
    options = minecraft_launcher_lib.utils.generate_test_options()
    mods_url = 'https://github.com/jamesfimmer/JFCRAFT-MODS/raw/main/mods.zip'
    mods_folder = minecraft_directory
    print(mods_folder)
    response = requests.get(mods_url)
    with open('mods.zip', 'wb') as f:
        f.write(response.content)
        # Распаковка архива
    shutil.unpack_archive('mods.zip', mods_folder, 'zip')

    os.remove('mods.zip')

    print("Запуск")
    subprocess.run(minecraft_launcher_lib.command.get_minecraft_command('1.19.2-forge-43.3.5', minecraft_directory, options))
    return


if __name__ == '__main__':
    main()
