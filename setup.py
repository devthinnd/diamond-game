import PyInstaller.__main__

PyInstaller.__main__.run([
    'diamond-game.py',
    '--onefile',
    '--windowed',
    '--icon=app.ico'
])