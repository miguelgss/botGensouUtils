cd src
pyinstaller --onefile main.py -n "$1"
wine pyinstaller --hidden-import=discord --onefile main.py -n "$1"
mkdir specs
mv *.spec specs/
cd ..
