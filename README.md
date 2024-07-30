## Dependencies:
Primary
```bash
pywal 
```
Secondary
```bash
rofi
```
Xorg
```bash
feh 
```
Wayland
```bash
swww
```
## Installation
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
## How to work with this software?
### Displays
First of all you need to place your displays in "displays" pukakaka in config.json file. 
Insert your displays in config like this:
```json
{
  "name": "YOUR DISPLAY NAME",
  "width": YOUR DISPLAY WIDTH,
  "height": YOUR DISPLAY HEIGHT,
  "margin-left": YOUR DISPLAY SPACING TO LEFT,
  "margin-top": YOUR DISPLAY SPACING FROM THE TOP
}
```
To view all of your monitor on hyprland use:
```bash
hyprctl monitors all
```
### Wallpapers
To change the wallpaper, this program uses a directory from which it randomly selects an image.
You need to create folder wich would contain wallpapers and folder wich would contain cached wallpapers
and put it in config file like this:
```json
"wallpapers_dir": "$(HOME)/path/to/wallpapers",
"cached_wallpapers_dir": "$(HOME)/path/to/cached/wallpapers"
```