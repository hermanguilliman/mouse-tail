from tkinter import *
from ctypes import windll, Structure, c_long, byref

width = 100
height = 50
refresh_rate = 1
label_color = '#F2D632'
label_font = ('Terminal', 8, 'bold')
root_transparent = 1


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y


def main():
    root = Tk()
    root.overrideredirect(True)
    root.attributes('-topmost',True)
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "#FF00FF")
    root.wm_attributes("-alpha", root_transparent)
    root.configure(width=width, height=height, background="#FF00FF")    
    root.geometry(f"{width}x{height}")
    
    label = Label(root, background='#FF00FF', foreground=label_color, font=label_font, justify="left")
    label.pack(fill="both", expand=True)
    
    def update():
        mouse_x, mouse_y = queryMousePosition()
        label['text'] = f'x:{mouse_x} y:{mouse_y}'
        root.geometry(f'{width}x{height}+{mouse_x+5}+{mouse_y+5}')
        root.after(refresh_rate, update)

    update()
    root.mainloop()

if __name__ == "__main__":
    main()