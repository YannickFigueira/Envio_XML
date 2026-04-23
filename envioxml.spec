# programaigreja.spec
block_cipher = None

a = Analysis(
    ['envioxml.py'],   # arquivo principal
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['crypto', 'dados', 'enviaremail', 'verificarversao', 'janelaconfig', 'metodos', 'relatorio', 'telegrambot', 'xmlreadnota', 'telegram', pystray],  # módulos auxiliares
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='envioxml',
    debug=False,
    strip=False,
    upx=True,
    console=False,  # sem janela de prompt
)

