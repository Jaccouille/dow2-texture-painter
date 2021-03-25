import tkinter as tk
from tkinter import colorchooser
from functools import partial

COLOR_BOX_SIZE = 90
COLOR_BTN_HEIGHT = 26


class FrameColorChooser(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super(FrameColorChooser, self).__init__(master=master, cnf={}, **kw)
        self.color_boxes = []
        self.color_buttons = []

        # Color Dialog that open upon btn click
        self.color_dialog = colorchooser.Chooser(self)

        self.initialize()

    def initialize(self):
        for i in range(0, 4):
            self.color_boxes.append(
                tk.Canvas(
                    self,
                    bg="gray",
                    relief=tk.RAISED,
                    bd=2,
                    height=COLOR_BOX_SIZE,
                    width=COLOR_BOX_SIZE,
                )
            )
            self.color_boxes[i].bind(
                "<Button-1>", partial(self.apply_color, i))
            self.color_boxes[i].place(
                anchor=tk.NW, x=COLOR_BOX_SIZE * i, y=COLOR_BTN_HEIGHT
            )
            self.color_buttons.append(
                tk.Button(
                    self,
                    text=f"Choose Color {i}",
                    wraplength=COLOR_BOX_SIZE,
                    relief=tk.RAISED,
                    bd=2,
                    command=partial(self.apply_color, i),
                )
            )
            self.color_buttons[i].place(
                anchor=tk.NW, x=COLOR_BOX_SIZE * i + i * 1, y=0)
        self.draw_rgb_value()

    def apply_color(self, btn_idx: int, Event=None):
        _, color = self.color_dialog.show()
        if color is not None:
            self.color_boxes[btn_idx]["bg"] = color
            self.draw_rgb_value()
            self._root().refresh_workspace()

    def draw_rgb_value(self):
        for color_box in self.color_boxes:
            color = str(color_box["bg"])
            color_box.delete("all")
            color_box.create_text(
                COLOR_BOX_SIZE / 2,
                COLOR_BOX_SIZE / 2,
                text=color,
                font=("Arial", 10, "bold"),
            )
