# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('silkware/config', 'config')],
    hiddenimports=['Xlib.display', 'Xlib.X', 'Xlib.protocol', 'Xlib.error', 'Xlib.xobject', 'Xlib.ext', 'Xlib.keysymdef', 'Xlib.threaded', 'Xlib.Xatom', 'Xlib.Xcursorfont', 'Xlib.XK', 'Xlib.Xutil', 'Xlib.xauth'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Silkware',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
