import tkinter as tk
import os
from tkinter import colorchooser, filedialog
from functools import partial
from src.color_pattern_handler import army_color_pattern
from src.constant import OPEN_FILETYPES, SAVE_EXT_LIST, ColorOps


COLOR_BOX_SIZE = 90
COLOR_BTN_HEIGHT = 26


class FrameChannelList(tk.LabelFrame):
    def __init__(self, master=None, cnf={}, **kw):
        super(FrameChannelList, self).__init__(master=master, cnf={}, **kw)

        # Channel List Box
        self.lb = tk.Listbox(self, selectmode=tk.MULTIPLE, height=4, width=9)
        self.lb.insert(0, "0 Red")
        self.lb.insert(1, "1 Green")
        self.lb.insert(2, "2 Blue")
        self.lb.insert(3, "3 Alpha")
        self.lb.pack(side=tk.TOP, fill=tk.Y)

        # Add alpha BTN
        self.apply_alpha = tk.BooleanVar()
        self.add_alpha = tk.Checkbutton(
            self,
            text="Apply alpha",
            variable=self.apply_alpha,
            onvalue=1,
            offvalue=0,
            height=2,
            command=self._root().on_apply_alpha_toggle,
        )
        self.add_alpha.pack(side=tk.TOP, fill=tk.X)


class FrameColorChooser(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super(FrameColorChooser, self).__init__(master=master, cnf={}, **kw)
        self.color_boxes = []
        self.color_buttons = []
        self.initialize()

    def initialize(self):
        for i in range(0, 4):
            self.color_boxes.append(
                tk.Canvas(
                    self,
                    bg="#808080",
                    relief=tk.RAISED,
                    bd=2,
                    height=COLOR_BOX_SIZE,
                    width=COLOR_BOX_SIZE,
                )
            )
            self.color_boxes[i].bind("<Button-1>", partial(self.apply_color, i))
            self.color_boxes[i].place(
                anchor=tk.NW, x=COLOR_BOX_SIZE * i, y=COLOR_BTN_HEIGHT
            )
            self.color_buttons.append(
                tk.Button(
                    self,
                    text=f"Choose Color {i + 1}",
                    wraplength=COLOR_BOX_SIZE,
                    relief=tk.RAISED,
                    bd=2,
                    command=partial(self.apply_color, i),
                )
            )
            self.color_buttons[i].place(anchor=tk.NW, x=COLOR_BOX_SIZE * i + i * 1, y=0)
        self.draw_rgb_value()

    def apply_color(self, btn_idx: int, Event=None):
        # Color Dialog that open upon btn click
        _, color = colorchooser.askcolor(self.color_boxes[btn_idx]["bg"])
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


class FrameSlider(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super(FrameSlider, self).__init__(master=master, cnf={}, **kw)

        # Brightness slider
        self.brightness_slider = tk.Scale(
            self,
            label="Brightness",
            length=150,
            from_=0.0,
            to=150.0,
            orient=tk.HORIZONTAL,
            command=self._root().on_slider_update,
        )
        self.brightness_slider.pack(side=tk.TOP, fill=tk.X)

        # Contrast slider
        self.contrast_slider = tk.Scale(
            self,
            label="Contrast",
            length=200,
            from_=0.0,
            to=200.0,
            orient=tk.HORIZONTAL,
            command=self._root().on_slider_update,
        )
        self.contrast_slider.pack(side=tk.TOP, fill=tk.X)

class FrameColorOps(tk.LabelFrame):
    def __init__(self, master=None, cnf={}, **kw):
        super(FrameColorOps, self).__init__(master=master, cnf={}, **kw)
        self.color_operation_btn = {op.value:None for op in ColorOps}
        self.var = tk.StringVar(value=ColorOps.OVERLAY.value)
        for op_name, value in self.color_operation_btn.items():
            value = tk.Radiobutton(
                self,
                text=op_name,
                variable=self.var,
                value=op_name,
                command=self._root().color_operation_update,
            )
            value.pack(side=tk.LEFT)


class FramePatternList(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super(FramePatternList, self).__init__(master=master, cnf={}, **kw)
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lb = tk.Listbox(
            self, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.config(command=self.lb.yview)

        self.load_pattern_list()
        self.save_pattern = tk.Button(
            self, text="Save pattern", command=self._root().save_pattern
        )
        self.save_pattern.pack(side=tk.TOP, fill=tk.X)

        self.delete_pattern = tk.Button(
            self, text="Delete pattern", command=self._root().delete_pattern
        )
        self.delete_pattern.pack(side=tk.TOP, fill=tk.X)

    def load_pattern_list(self):
        self.lb.delete(0, "end")
        for idx, pattern_name in enumerate(army_color_pattern):
            self.lb.insert(idx, pattern_name)
        self.lb.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class BatchEditTopLevel(tk.Toplevel):
    def __init__(self, master=None, cnf={}, **kw):
        super(BatchEditTopLevel, self).__init__(master=master, cnf={}, **kw)

        self.initialize()

    def initialize(self):
        # Source format Checkbox list
        self.source_format_list = []
        self.frame_source_format = tk.LabelFrame(self, text="Source formats")
        self.frame_source_format.pack(side=tk.TOP, fill=tk.BOTH)
        for idx, filetype in enumerate(OPEN_FILETYPES[1:]):
            self.source_format_list.append(
                tk.Checkbutton(
                    self.frame_source_format,
                    text=filetype[1][1:].upper(),
                    onvalue=True,
                    offvalue=False,
                )
            )
            self.source_format_list[idx].pack(side=tk.LEFT)
        # Setting default input format
        self.source_format_list[0].toggle()

        # Destination Format Option Menu
        self.frame_destination_format = tk.Frame(self)
        self.frame_destination_format.pack(side=tk.TOP, fill=tk.X)
        tk.Label(self.frame_destination_format, text="Destination format:").pack(
            side=tk.LEFT
        )
        self.dest_format = tk.StringVar(self)
        self.dest_format.set(SAVE_EXT_LIST[0].upper())
        self.dest_menu = tk.OptionMenu(
            self.frame_destination_format,
            self.dest_format,
            *[fmt.upper() for fmt in SAVE_EXT_LIST],
        )
        self.dest_menu.pack(side=tk.LEFT)
        tk.Button(
            self.frame_destination_format,
            text="Process Batch Edit",
            command=self._root().batch_edit,
        ).pack(side=tk.LEFT)


        def select_folder(folder_path, Event=None):
            folder_path.set(filedialog.askdirectory(initialdir=os.curdir))

        def widget_entry_template(
            frame,
            label,
            starting_value="",
            entry_width=60,
            label_width=len("Destination folder:"),
        ):
            entry_frame = tk.Frame(frame)
            entry_frame.pack(side=tk.TOP, fill=tk.X)
            tk.Label(entry_frame, text=label, width=label_width, anchor=tk.W).pack(
                side=tk.LEFT
            )
            entry_frame.entry_value = tk.StringVar(value=starting_value)
            entry_path = tk.Entry(
                entry_frame,
                textvariable=entry_frame.entry_value,
                width=60,
                exportselection=0,
            )
            entry_path.pack(side=tk.LEFT)
            tk.Button(
                entry_frame,
                text="...",
                command=lambda: (select_folder(entry_frame.entry_value)),
            ).pack(side=tk.LEFT)
            return entry_frame

        self.frame_batch_src_path = widget_entry_template(self, "Source folder:")
        self.frame_batch_dest_path = widget_entry_template(self, "Destination folder:")
