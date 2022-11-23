from tkinter import Tk, Label
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


def load_config(path: str) -> Settings:
    """Load settings from ini file

    Args:
        path (str): path to the config file

    Returns:
        Settings: representation class of custom settings
    """
    config = configparser.ConfigParser()
    config.read(path)
    config = Settings(**config['settings'])
    return config


class POINT(Structure):
    """Structure for storing x and y points
    """
    _fields_ = [("x", c_long), ("y", c_long)]


def getMousePosition() -> tuple:
    """Return mouse coordinates x and y

    Returns:
        tuple: x, y mouse coordinates
    """
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y


def main() -> None:
    """Create main window, label and loop window update
    """
    root = Tk()
    config = load_config('config.ini')
    root.overrideredirect(True)
    root.attributes('-topmost',True)
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "#FF00FF")
    root.wm_attributes("-alpha", config.root_transparent)
    root.configure(width=config.width,
                   height=config.height,
                   background="#FF00FF")
    root.geometry(f"{config.width}x{config.height}")
    
    # Text label for displaying coordinates
    label = Label(root,
                  background='#FF00FF',
                  foreground=config.font_color,
                  font=(config.font_family,
                        config.font_size,
                        config.font_weight),
                  justify="left")
    label.pack(fill="both", expand=True)
    
    # Infinite window update
    def update() -> None:
        mouse_x, mouse_y = getMousePosition()
        label['text'] = f'x:{mouse_x} y:{mouse_y}'
        root.geometry(f'{config.width}x{config.height}+{mouse_x+5}+{mouse_y+5}')
        root.after(config.refresh_rate, update)

    # Entrance to the loop
    update()
    root.mainloop()


if __name__ == "__main__":
    main()