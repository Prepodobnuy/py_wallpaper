```bash
git clone https://github.com/Prepodobnuy/py_wallpaper.git
cd py_wallpaper
python -m venv env
. env/bin/activate
pip install pyinstaller pillow
pyinstaller --clean --onefile --name py_wallpaper wallpaper.py
chmod +X dist/py_wallpaper
sudo rm /usr/bin/py_wallpaper
sudo mv dist/py_wallpaper /usr/bin/py_wallpaper
mkdir ~/.config/py_wallpaper
mv config.json ~/.config/py_wallpaper/config.json
mv templates.json ~/.config/py_wallpaper/templates.json
cd ..
rm -rf py_wallpaper
```