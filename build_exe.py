"""Build the Windows launcher into dist/JFCRAFT.exe.

Run from the project root:
    python build_exe.py
"""
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
SPEC = ROOT / 'jfcraft.spec'
DIST = ROOT / 'dist'


def run(command):
    print('>', ' '.join(map(str, command)), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main():
    if not SPEC.is_file():
        raise SystemExit('Не найден jfcraft.spec. Запусти файл из проекта JFCRAFT.')
    try:
        import tkinter
        tkinter.Tcl().eval('info patchlevel')
    except Exception as error:
        raise SystemExit('В текущем Python не установлен Tkinter/Tcl: ' + str(error))

    pyinstaller = ROOT / '.buildenv' / 'Scripts' / 'pyinstaller.exe'
    if not pyinstaller.is_file():
        pyinstaller = Path(sys.executable).with_name('pyinstaller.exe')
    if not pyinstaller.is_file():
        raise SystemExit('PyInstaller не найден. Установи зависимости из requirements.txt.')
    run([sys.executable, ROOT / 'tools' / 'make_icon.py'])

    run([pyinstaller, '--clean', '--noconfirm', '--distpath', DIST, SPEC])
    result = DIST / 'JFCRAFT.exe'
    if not result.is_file():
        raise SystemExit('Сборка завершилась без dist/JFCRAFT.exe')
    print(f'Готово: {result}')


if __name__ == '__main__':
    main()
