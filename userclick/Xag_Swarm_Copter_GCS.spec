# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Xag_Swarm_Copter_GCS.py'],
             pathex=['D:\\plane\\dhaksha-server\\userclick'],
             binaries=[],
             datas=[],
             hiddenimports=['pywintypes', 'pythoncom'],
             hookspath=[],
             hooksconfig={},
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
          name='Xag_Swarm_Copter_GCS',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='D:\\plane\\GCS-live\\assets\\icons\\win\\MIT.ico')
