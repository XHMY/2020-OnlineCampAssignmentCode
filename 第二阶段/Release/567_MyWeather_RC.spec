# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['/Users/yokey/OneDrive/吉珠/Project/大一下线上工作室/code/Release/567_MyWeather_RC.py'],
             pathex=['/Users/yokey/OneDrive/吉珠/Project/大一下线上工作室/code/Release'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='567_MyWeather_RC',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
