import os
import tkinter as tk
from constant import OPEN_FILETYPES, SAVE_EXT_LIST
from tkinter import filedialog


class FrameBatchTool(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super(FrameBatchTool, self).__init__(master=master, cnf={}, **kw)

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

        # Destination Format Option Menu
        self.frame_destination_format = tk.Frame(self)
        self.frame_destination_format.pack(side=tk.TOP, fill=tk.X)
        tk.Label(self.frame_destination_format,
                 text="Destination format:").pack(

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
            tk.Label(
                entry_frame,
                text=label,
                width=label_width,
                anchor=tk.W).pack(
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

        self.frame_batch_src_path = widget_entry_template(
            self, "Source folder:")
        self.frame_batch_dest_path = widget_entry_template(
            self, "Destination folder:")
