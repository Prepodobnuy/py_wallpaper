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

## Dependencies
Primary:
```bash
pywal 
```
Secondary:
```bash
rofi
```
Xorg:
```bash
feh 
```
Wayland:
```bash
swww
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
To set wallpaper on wayland you need [swww](https://github.com/LGFae/swww)
To set wallpaper on xorg you need [feh](https://github.com/derf/feh)
To configure swww params, edit "swww_params" variable in config.json:
```json
"swww_params": "--transition-fps 165 --transition-step 10 --transition-duration 2 -f Nearest -t any"
```
### Pywal, colors, /r/unixpron 
With this AMAZING program you can automatically change colors depending on the wallpaper to be setted.
Unknown to anyone, but very cool software named [pywal](https://github.com/dylanaraps/pywal) is responsible for this.
To use [pywal](https://github.com/dylanaraps/pywal) set "use_pawal" option to true in your config.json file:
```json
"use_pywal": true
```
Also you can select another pywal backend:
```json
"wal_backend": "colorz"
```
Or generate light color theme instead of conformist dark theme:
```json
"light_theme": true
```
### Color variables 
Color variables is needed to paste [pywal](https://github.com/dylanaraps/pywal) colors in your config files.
To configure your color variables you need to paste them into config.json:
```json
"color_variables": [
  {
    "name": "(color0)",
    "value": 0
  },
  {
    "name": "(color1)",
    "value": 1
  },
  {
    "name": "(color2)",
    "value": 2
  }
]
```
"name" is responsible for text wich would be replaced with our color
and "value" is responsible for pywal color wich will replace "name".
### Templates
This software also can change configs of another programs installed on your computer
To do this incredible feature you need to clone your config file and replace all colors with your color variables
Let's look at this feature using the example of the [alacritty](https://github.com/alacritty/alacritty) config:
Template config:
```toml
[colors.bright]
black = (color0)
red = (color1)
green = (color2)
yellow = (color3)
blue = (color4)
magenta = (color5)
cyan = (color6)
white = (color7)

[colors.normal]
black = (color0)
red = (color1)
green = (color2)
yellow = (color3)
blue = (color4)
magenta = (color5)
cyan = (color6)
white = (color7)

[colors.primary]
background = (color0)
foreground = (color15)

[font]
size = 9

[font.bold]
family = "JetBrainsMono Nerd Font"
style = "Bold"

[font.bold_italic]
family = "JetBrainsMono Nerd Font"
style = "Bold Italic"

[font.italic]
family = "JetBrainsMono Nerd Font"
style = "Italic"

[font.normal]
family = "JetBrainsMono Nerd Font"
style = "Regular"

[window.padding]
x = 2
y = 2
```
Resulted config:
```toml
[colors.bright]
black = "#121c06"
red = "#9D9761"
green = "#629DAC"
yellow = "#66AEBF"
blue = "#9BB0AD"
magenta = "#AFBCB1"
cyan = "#E7D7AB"
white = "#cfdadb"

[colors.normal]
black = "#121c06"
red = "#9D9761"
green = "#629DAC"
yellow = "#66AEBF"
blue = "#9BB0AD"
magenta = "#AFBCB1"
cyan = "#E7D7AB"
white = "#cfdadb"

[colors.primary]
background = "#121c06"
foreground = "#cfdadb"

[font]
size = 9

[font.bold]
family = "JetBrainsMono Nerd Font"
style = "Bold"

[font.bold_italic]
family = "JetBrainsMono Nerd Font"
style = "Bold Italic"

[font.italic]
family = "JetBrainsMono Nerd Font"
style = "Italic"

[font.normal]
family = "JetBrainsMono Nerd Font"
style = "Regular"

[window.padding]
x = 2
y = 2
```
As you can see py_wallpaper changed color variables to actual colors.
To make this software reads file templates.json.
Lets take a look:
```json
{
  "templates": [
    {
      "template_path": "~/path/to/template/alacritty.toml",    
      "config_path": "~/.config/alacritty/alacritty.toml",
      "use_quotes": 0,
      "use_sharps": 1,
      "opacity": 0,
      "command": ""    
    }
  ]
}
```
"template_path" is a path to template file
"config_path" is a path to config file
"use_quotes" is a 0/1 variable wich is wraps your color with ": 000000 -> "000000"
"use_sharps" is a 0/1 variable wich is adds # before your color: 000000 -> #000000
"opacity" is a 0/ff variable wich is adds value after your color: 000000 -> 000000ff
if "opacity" is setted to 0 it would not add any value.
"command" is a shell commands wich would start after template is executed
glhf