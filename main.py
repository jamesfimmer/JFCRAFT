import minecraft_launcher_lib
import subprocess


def main():
    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('.minecraft', '.jfcraft')
    callback = {
        "setStatus": lambda text: print(text, end='\n'),
    }
    minecraft_version = input()
    minecraft_launcher_lib.install.install_minecraft_version(minecraft_version, minecraft_directory, callback)
    options = minecraft_launcher_lib.utils.generate_test_options()
    print("Идёт крутой запуск майнкрафта")
    subprocess.run(minecraft_launcher_lib.command.get_minecraft_command(minecraft_version, minecraft_directory, options))
    return


if __name__ == '__main__':
    main()
