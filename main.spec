# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules
import tkinter
tkinter.Tcl().eval('info patchlevel')
from PyInstaller.utils.hooks.tcl_tk import tcltk_info
if not tcltk_info.available:
    raise RuntimeError('Tk/Tcl unavailable: refusing to build a broken launcher')


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('packs', 'packs')],
    hiddenimports=['minecraft_launcher_lib', '_tkinter', 'tkinter', 'tkinter.ttk'] + collect_submodules('tkinter'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='JFCRAFT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
