from tkinter import *
from ctypes import windll, Structure, c_long, byref
import configparser
from dataclasses import dataclass

@dataclass
class Settings:
    width: int
    height: int
    refresh_rate: int
    font_family: str
    font_size: int
    font_weight: str
    font_color: str
    root_transparent: float


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)
    config = Settings(**config['settings'])
    return config

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y


def main():
    root = Tk()
    config = load_config('config.ini')
    root.overrideredirect(True)
    root.attributes('-topmost',True)
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "#FF00FF")
    root.wm_attributes("-alpha", config.root_transparent)
    root.configure(width=config.width, height=config.height, background="#FF00FF")    
    root.geometry(f"{config.width}x{config.height}")
    
    label = Label(root, background='#FF00FF', foreground=config.font_color, font=(config.font_family, config.font_size, config.font_weight), justify="left")
    label.pack(fill="both", expand=True)
    
    def update():
        mouse_x, mouse_y = queryMousePosition()
        label['text'] = f'x:{mouse_x} y:{mouse_y}'
        root.geometry(f'{config.width}x{config.height}+{mouse_x+5}+{mouse_y+5}')
        root.after(config.refresh_rate, update)

    update()
    root.mainloop()


if __name__ == "__main__":
    main()