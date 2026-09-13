# Build: python -m PyInstaller --clean --noconfirm jfcraft.spec
a = Analysis(['main.py'], pathex=[], binaries=[], datas=[('packs', 'packs')],
             hiddenimports=['minecraft_launcher_lib'], hookspath=[], hooksconfig={},
             runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name='JFCRAFT', debug=False,
          bootloader_ignore_signals=False, strip=False, upx=False,
          console=False, disable_windowed_traceback=False)
