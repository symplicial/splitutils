# -*- mode: python ; coding: utf-8 -*-

# split_sounds
split_sounds_a = Analysis(
    ['split_sounds\\split_sounds.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
split_sounds_pyz = PYZ(split_sounds_a.pure)
split_sounds_exe = EXE(
    split_sounds_pyz,
    split_sounds_a.scripts,
    [],
    exclude_binaries=True,
    name='split_sounds',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# worst_viable_run
worst_viable_run_a = Analysis(
    ['worst_viable_run\\worst_viable_run.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
worst_viable_run_pyz = PYZ(worst_viable_run_a.pure)
worst_viable_run_exe = EXE(
    worst_viable_run_pyz,
    worst_viable_run_a.scripts,
    [],
    exclude_binaries=True,
    name='worst_viable_run',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# collect
coll = COLLECT(
    split_sounds_exe,
    split_sounds_a.binaries,
    split_sounds_a.datas,
    worst_viable_run_exe,
    worst_viable_run_a.binaries,
    worst_viable_run_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='split_sounds',
)
