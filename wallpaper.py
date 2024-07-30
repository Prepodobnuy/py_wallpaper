import os
import sys
import time
import random
import subprocess

import json

from PIL import Image


HOME = os.getenv("HOME")
DEBUG = False


def runrofi(wallpapers) -> list[str]:
    result = subprocess.run(
        ["rofi", "-dmenu", "-p"],
        input="\n".join(wallpapers).encode(),
        stdout=subprocess.PIPE,
    )
    return result.stdout.decode()

def in_args(params: list[str]) -> bool:
    for param in params:
        if param in sys.argv:
            return True
    return False

def get_value_from_args(params: list[str]) -> str | None:
    for param in params:
        if param in sys.argv:
            return sys.argv[sys.argv.index(param) + 1]
    return None

class Config(object):
    def __init__(self) -> None:
        self.config_path = f'{HOME}/.config/py_wallpaper/config.json'
        if in_args(["-c", "--conf"]): self.config_path = get_value_from_args(["-c", "--conf"])
        with open(self.config_path) as file:
            self.config_data = json.loads(file.read())

        self.raw_displays_params: dict = self.try_to_set("displays")

        self.color_variables: list[dict] = self.try_to_set("color_variables")

        self.wallpapers_dir: str = f"{HOME}".join(self.try_to_set("wallpapers_dir").split("$(HOME)"))
        self.cached_wallpapers_dir: str = f"{HOME}".join(self.try_to_set("cached_wallpapers_dir").split("$(HOME)"))
        self.wal_colors_dir: str = f"{HOME}".join(self.try_to_set("wal_colors_dir").split("$(HOME)"))
        self.template_config_dir: str = f"{HOME}".join(self.try_to_set("template_config").split("$(HOME)"))
        self.wal_backend: str = self.try_to_set("wal_backend")
        self.wal_bg_color: str = self.try_to_set("wal_bg_color")
        self.swww_params: str = self.try_to_set("swww_params")
        self.sleep_time: int = self.try_to_set("sleep_time")
        self.light_theme: bool = self.try_to_set("light_theme")
        self.resize_displays: bool = self.try_to_set("resize_displays")
        self.apply_templates: bool = self.try_to_set("apply_templates")
        self.use_pywal: bool = self.try_to_set("use_pywal")

        self.read_args()

    def try_to_set(self, param: str) -> any:
        try:
            return self.config_data[param]
        except Exception as e:
            return None
    
    def read_args(self) -> None:
        runcount = -1
        if in_args(["-wd", "--wallpaper-dir"]):          self.wallpapers_dir        = get_value_from_args(["-wd", "--wallpaper-dir"])
        if in_args(["-cwd", "--cached-wallpaper-dir"]):  self.cached_wallpapers_dir = get_value_from_args(["-cwd", "--cached-wallpaper-dir"])
        if in_args(["-pcd", "--pywal-colors-dir"]):      self.wal_colors_dir        = get_value_from_args(["-pcd", "--pywal-colors-dir"])
        if in_args(["-t", "--temp"]):                    self.template_config_dir   = get_value_from_args(["-t", "--temp"])
        if in_args(["-pb", "--pywal-backend"]):          self.wal_backend           = get_value_from_args(["-pb", "--pywal-backend"])
        if in_args(["-pbc", "--pywal-backgroundcolor"]): self.wal_bg_color          = get_value_from_args(["-pbc", "--pywal-backgroundcolor"])
        if in_args(["--swww"]):                          self.swww_params           = get_value_from_args(["--swww"])
        if in_args(["-s", "--sleep-time"]):              self.sleep_time            = int(get_value_from_args(["-s", "--sleep-time"]))
        if in_args(["-l", "--light"]):                   self.light_theme           = True
        if in_args(["--resize-displays"]):               self.resize_displays       = True
        if in_args(["--cache-all"]):
            for wallpaper_name in os.listdir(self.wallpapers_dir):
                cache_wallpaper(wallpaper_name=wallpaper_name, wallpaper_path=f'{self.wallpapers_dir}/{wallpaper_name}')
                sys.exit(1)
        if in_args(["--once"]):
            runcount = 1
        wallpaper_name = random.choice(os.listdir(self.wallpapers_dir))
        if in_args(["-r", "--rofi"]):
            wallpaper_name = runrofi(os.listdir(self.wallpapers_dir))
            runcount = 1

        self.runcount = runcount
        self.wallpaper_name = wallpaper_name


CONFIG = Config()


class Display(object):
    def __init__(self, name:str, width:int, height:int, margin_x:int=0, margin_y:int=0) -> None:
        self.name: str = name
        self.w: int = width
        self.h: int = height
        self.x: int = margin_x
        self.y: int = margin_y
        self.image: Image = None

    def max_width(displays: list) -> int:
        res = 0
        for display in displays:
            res = display.w + display.x if display.w + display.x > res else res
        return res

    def max_height(displays: list) -> int:
        res = 0
        for display in displays:
            res = display.h + display.y if display.h + display.y > res else res
        return res


class Template(object):
    def __init__(self, templatepath:str, configfilepath:str, usequotes:bool=False, usesharps:bool=False, command:str=None, opacity:str="") -> None:
        self.templatefilepath:str = templatepath
        self.configfilepath:str = configfilepath
        self.executeAfter:str = command
        self.usequotes:bool = usequotes
        self.usesharps:bool = usesharps
        self.opacity:str = opacity

    def apply(self, colors: list[str]) -> None:
        variables = CONFIG.color_variables

        with open(self.templatefilepath, "r") as template:
            data = template.read()

        for variable in variables:
            data = data.split(variable["name"])
            color = colors[variable["value"]]
            tmp = color + self.opacity

            if not self.usesharps:
                tmp = tmp[1::]
            if self.usequotes:
                tmp = f'"{tmp}"'

            data = f"{tmp}".join(data)

        with open(self.configfilepath, "w") as result:
            result.write(data)

        self.execute()

    def execute(self) -> None:
        if self.executeAfter != None:
            os.popen(self.executeAfter)


def read_templates() -> list[Template]:
    res: list[Template] = []

    with open(CONFIG.template_config_dir) as file:
        json_data = json.loads(file.read())

    for raw_template in json_data["templates"]:
        template = Template(
            templatepath=f'{HOME}/{raw_template["template_path"][2::]}' if raw_template["template_path"][0] == "~" else raw_template["template_path"],
            configfilepath=f'{HOME}/{raw_template["config_path"][2::]}' if raw_template["config_path"][0] == "~" else raw_template["config_path"],
            usequotes=raw_template["use_quotes"],
            usesharps=raw_template["use_sharps"],
            opacity=raw_template["opacity"] if raw_template["opacity"] != 0 else "",
            command=raw_template["command"],
        )
        res.append(template)

    return res


def read_displays() -> list[Display]:
    res: list[Display] = []

    for display in CONFIG.raw_displays_params:
        tmp = Display(
            name=display["name"],
            width=display["width"],
            height=display["height"],
            margin_x=display["margin-left"],
            margin_y=display["margin-top"],
        )
        res.append(tmp)

    return res


def resize_displays(displays: list[Display], image: Image) -> list[Display]:
    width, height = image.size
    max_width = Display.max_width(displays)

    width_dif = width / max_width

    for display in displays:
        display.w = int(display.w * width_dif)
        display.h = int(display.h * width_dif)
        display.x = int(display.x * width_dif)
        display.y = int(display.y * width_dif)

    max_height = Display.max_height(displays)
    height_dif = height / max_height

    if height_dif < 1:
        for display in displays:
            display.w = int(display.w * height_dif)
            display.h = int(display.h * height_dif)
            display.x = int(display.x * height_dif)
            display.y = int(display.y * height_dif)

    return displays


def resize_wallpaper(displays: list[Display], image: Image) -> Image:
    width, height = image.size
    max_width = Display.max_width(displays)

    width_dif: float = max_width / width

    new_width = int(width * width_dif)
    new_heigth = int(height * width_dif)

    image = image.resize((new_width, new_heigth))

    max_height = Display.max_height(displays)
    width, height = image.size
    height_dif = max_height / height

    if height_dif > 1:
        new_width = int(width * height_dif)
        new_heigth = int(height * height_dif)
        image = image.resize((new_width, new_heigth))

    return image


def split_wallpaper(displays: list[Display], image: Image) -> list[Display]:
    for display in displays:
        display.image = image.crop(
            (display.x, display.y, display.w + display.x, display.h + display.y)
        )

    return displays


def cache_wallpaper(wallpaper_path:str, wallpaper_name:str) -> None:
    cache_is_needed = False

    for display in read_displays():
        if not os.path.exists(f'{CONFIG.cached_wallpapers_dir}/{display.name}-{display.w}.{display.h}.{display.x}.{display.y}{wallpaper_name.split('.')[0]}.png'):
            cache_is_needed = True
            break

    if not cache_is_needed: return

    displays: list[Display] = read_displays()
    image: Image = Image.open(wallpaper_path)

    if CONFIG.resize_displays:
        displays = resize_displays(displays, image)
    else:
        image = resize_wallpaper(displays, image)

    displays = split_wallpaper(displays, image)

    for display in displays:
        display.image.save(
            f'{CONFIG.cached_wallpapers_dir}/{display.name}-{display.w}.{display.h}.{display.x}.{display.y}{wallpaper_name.split('.')[0]}.png',
            optimize=True,
            quality=100,
        )


def apply_templates() -> None:
    templates: list[Template] = read_templates()

    with open(f"{CONFIG.wal_colors_dir}") as file:
        colors = (file.read()).split("\n")

    for template in templates:
        template.apply(colors)


def change_colors(wallpaper_path:str) -> None:
    if "\n" in wallpaper_path:
        wallpaper_path = wallpaper_path[::-1][1::][::-1]
    pywal_command: str = f"python -m pywal -n -e -q {'-l' if CONFIG.light_theme else ''} {"-b " + CONFIG.wal_bg_color if CONFIG.wal_bg_color else ""} -i {wallpaper_path} --backend {CONFIG.wal_backend} "

    os.system(pywal_command)


def set_wallpapper(wallpaper_path:str, wallpaper_name:str) -> None:
    displays: list[Display] = read_displays()

    for display in displays:
        xorg = False

        try: os.system(f"swww img {CONFIG.cached_wallpapers_dir}/{display.name}-{display.w}.{display.h}.{display.x}.{display.y}{wallpaper_name.split('.')[0]}.png -o {display.name} {CONFIG.swww_params}")
        except Exception:
            os.system(f"feh --bg-fill {wallpaper_path} --no-xinerama")
            xorg = True

        if xorg: break
    

def main(wallpaper_name: str, runcount: int) -> None:
    iteration = 0
    prev_wallpaper_name = None

    try:
        while iteration != runcount:
            if iteration > 0:
                time.sleep(CONFIG.sleep_time)
            while wallpaper_name == prev_wallpaper_name:
                wallpaper_name = random.choice(os.listdir(CONFIG.wallpapers_dir))
            prev_wallpaper_name = wallpaper_name

            wallpaper_path:str = f"{CONFIG.wallpapers_dir}/{wallpaper_name}"

            if CONFIG.use_pywal: change_colors(wallpaper_path)
            if CONFIG.apply_templates: apply_templates()
            cache_wallpaper(wallpaper_path, wallpaper_name)
            set_wallpapper(wallpaper_path, wallpaper_name)

            iteration += 1

    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(wallpaper_name=CONFIG.wallpaper_name, runcount=CONFIG.runcount)
