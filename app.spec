# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
  ('main.qml', '.'),
  ('FontLoaders.qml', '.'),
  ('util/helpers.js', 'util'),
  ('shared', 'shared'),
  ('views', 'views'),
  ('mock_data', 'mock_data')
]

a = Analysis(['app.py'],
             pathex=['.'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='LastRedux',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app')

app = BUNDLE(coll,
             name='LastRedux.app',
             icon=None,
             bundle_identifier=None)
