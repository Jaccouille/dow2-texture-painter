import os
import tkinter as tk
from tkinter import colorchooser, font
from PIL import (
    Image,
    ImageChops,
    ImageOps,
    ImageFont,
    ImageTk,
    ImageColor,
    ImageEnhance,
    ImageDraw,
)
from functools import partial
from tkinter import filedialog
from enum import Enum

VIEW_IMG_TOOL = 0
VIEW_BATCH_EDIT_TOOL = 1

path = os.path.dirname(__file__)

OPEN_FILETYPES = (
    ("all", (".dds", ".png", ".jpg", ".bmp", ".tga", ".blp")),
    ("Direct Draw Surface", ".dds"),
    ("Portable Network Graphics", ".png"),
    ("JPEG Image", ".jpg"),
    ("Bitmap", ".bmp"),
    ("True Vision Targa", ".tga"),
    ("Blizzard Texture", ".blp"),
)
SAVE_FILETYPES = (
    ("Portable Network Graphics", ".png"),
    ("JPEG Image", ".jpg"),
    ("Bitmap", ".bmp"),
    ("True Vision Targa", ".tga"),
)
COLOR_BOX_SIZE = 90
COLOR_BTN_HEIGHT = 26
FRAME_TOOL_HEIGHT = COLOR_BOX_SIZE + COLOR_BTN_HEIGHT + 12

DEFAULT_IMG_SIZE = 256


def create_placeholder_img():
    img = Image.new(
        mode="RGBA", size=(DEFAULT_IMG_SIZE, DEFAULT_IMG_SIZE), color="gray"
    )
    d1 = ImageDraw.Draw(img)
    d1.text(xy=(180, 256), fill="black", text="Image PlaceHolder")
    return img


class ArmyPainter(tk.Tk):
    def __init__(self):
        super().__init__()

        min_size = (DEFAULT_IMG_SIZE * 2 + 12, DEFAULT_IMG_SIZE + FRAME_TOOL_HEIGHT)
        dimension = f"{min_size[0]}x{min_size[1]}"
        self.geometry(dimension)
        self.minsize(min_size[0], min_size[1])
        self.title("Army Painter")
        self.tem_channels = []

        # Frame IMG Tool
        self.frame_img_tools = tk.Frame(
            self,
            width=DEFAULT_IMG_SIZE * 2,
            height=COLOR_BOX_SIZE + COLOR_BTN_HEIGHT,
            bd=2,
            relief=tk.RIDGE,
        )
        self.frame_img_tools.pack(side=tk.TOP, fill=tk.BOTH)

        # Frame Batch Tool
        self.frame_batch_tools = tk.Frame(
            self,
            width=DEFAULT_IMG_SIZE * 2,
            height=COLOR_BOX_SIZE + COLOR_BTN_HEIGHT,
            bd=2,
            relief=tk.RIDGE,
        )
        self.frame_batch_tools.pack_forget()
        self.define_frame_batch_tool()

        # Frame IMG
        self.frame_img = tk.Frame(self)
        self.frame_img.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        # TODO: refactor img variable
        self.img_og_dif = create_placeholder_img()
        self.img_dif = ImageTk.PhotoImage(self.img_og_dif)

        # Label SETTING DIF
        self.label_img_dif = tk.Label(
            self.frame_img, image=self.img_dif, relief=tk.RAISED
        )
        self.label_img_dif.pack(side=tk.LEFT, fill=tk.Y)

        self.img_og_tem = create_placeholder_img()
        self.img_tem = ImageTk.PhotoImage(self.img_og_tem)

        # LABEL SETTING TEM
        self.label_img_tem = tk.Label(
            self.frame_img, image=self.img_tem, relief=tk.RAISED
        )
        self.label_img_tem.pack(side=tk.LEFT, fill=tk.Y)

        # Color boxes
        self.frame_boxes = tk.Frame(
            self.frame_img_tools,
            relief=tk.SOLID,
            width=COLOR_BOX_SIZE * 4 + 4,
            height=COLOR_BTN_HEIGHT + COLOR_BOX_SIZE,
        )
        # self.frame_boxes.place(anchor=tk.NW)
        self.frame_boxes.pack(side=tk.LEFT, fill=tk.Y)

        self.color_boxes = []
        self.color_buttons = []
        for i in range(0, 4):
            self.color_boxes.append(
                tk.Canvas(
                    self.frame_boxes,
                    bg="gray",
                    relief=tk.RAISED,
                    bd=2,
                    height=COLOR_BOX_SIZE,
                    width=COLOR_BOX_SIZE,
                )
            )
            self.color_boxes[i].place(
                anchor=tk.NW, x=COLOR_BOX_SIZE * i, y=COLOR_BTN_HEIGHT
            )
            self.color_buttons.append(
                tk.Button(
                    self.frame_boxes,
                    text=f"Choose Color {i}",
                    wraplength=COLOR_BOX_SIZE,
                    relief=tk.RAISED,
                    bd=2,
                    command=partial(self.apply_color, i),
                )
            )
            self.color_buttons[i].place(anchor=tk.NW, x=COLOR_BOX_SIZE * i + 1, y=0)

        # Color Dialog that open upon btn click
        self.color_dialog = colorchooser.Chooser(self)

        # Channel List Frame
        self.frame_channel_list = tk.LabelFrame(
            self.frame_img_tools, text="RGBA Channel", relief=tk.RIDGE, bd=2
        )
        self.frame_channel_list.pack(side=tk.LEFT, fill=tk.Y)

        # Channel List Box
        self.lb = tk.Listbox(
            self.frame_channel_list, selectmode=tk.MULTIPLE, height=4, width=9
        )
        self.lb.insert(0, "0 Red")
        self.lb.insert(1, "1 Green")
        self.lb.insert(2, "2 Blue")
        self.lb.insert(3, "3 Alpha")
        self.bind("<<ListboxSelect>>", self.select_channel)
        self.lb.pack(side=tk.TOP, fill=tk.Y)

        # Add alpha BTN
        self.add_alpha = tk.Button(
            self.frame_channel_list, text="Apply alpha", command=self.apply_alpha
        )
        self.add_alpha.pack(side=tk.TOP, fill=tk.X)

        self.frame_sliders = tk.Frame(self.frame_img_tools, relief=tk.RIDGE, bd=2)
        self.frame_sliders.pack(side=tk.LEFT, fill=tk.Y)

        # Brightness slider
        self.brightness_slider = tk.Scale(
            self.frame_sliders,
            label="Brightness",
            length=150,
            from_=0.0,
            to=150.0,
            orient=tk.HORIZONTAL,
            command=self.adjust_brightness,
        )
        self.brightness_slider.pack(side=tk.TOP, fill=tk.X)

        # Contrast slider
        self.contrast_slider = tk.Scale(
            self.frame_sliders,
            label="Contrast",
            length=200,
            from_=0.0,
            to=200.0,
            orient=tk.HORIZONTAL,
            command=self.adjust_contrast,
        )
        self.contrast_slider.pack(side=tk.TOP, fill=tk.X)
        self.reset_workspace()

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(
            label="Open diffuse", command=self.open_diffuse, accelerator="Ctrl+O"
        )
        filemenu.add_command(
            label="Open channel file", command=self.open_channel, accelerator="Ctrl+A"
        )
        filemenu.add_command(label="Save", command=self.save, accelerator="Ctrl+S")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(
            label="Reset workspace", command=self.reset_workspace, accelerator="Ctrl+R"
        )
        menubar.add_cascade(label="Edit", menu=editmenu)

        self.tool_view = tk.IntVar()
        toolmenu = tk.Menu(menubar, tearoff=0)
        toolmenu.add_radiobutton(
            label="Image Tools",
            variable=self.tool_view,
            value=VIEW_IMG_TOOL,
            command=self.toggle_tool_view
        )
        toolmenu.add_radiobutton(
            label="Batch Edit Tools",
            variable=self.tool_view,
            value=VIEW_BATCH_EDIT_TOOL,
            command=self.toggle_tool_view
        )
        menubar.add_cascade(label="Tools", menu=toolmenu)

        self.bind("<Control-o>", self.open_diffuse)
        self.bind("<Control-a>", self.open_channel)
        self.bind("<Control-s>", self.save)
        self.bind("<Control-d>", self.batch_edit)
        self.bind("<Control-r>", self.reset_workspace)
        self.draw_rgb_value()

    def define_frame_batch_tool(self):
        # Source format Checkbox list
        self.source_format_list = []
        self.frame_source_format = tk.LabelFrame(
            self.frame_batch_tools, text="Source formats"
        )
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
        self.frame_destination_format = tk.Frame(self.frame_batch_tools)
        self.frame_destination_format.pack(side=tk.TOP, fill=tk.X)
        tk.Label(self.frame_destination_format, text="Destination format:").pack(
            side=tk.LEFT
        )
        self.dest_format = tk.StringVar(self)
        format_list = [fmt[1][1:].upper() for fmt in SAVE_FILETYPES]
        self.dest_format.set(format_list[0])
        self.dest_menu = tk.OptionMenu(
            self.frame_destination_format,
            self.dest_format,
            *format_list,
        )
        self.dest_menu.pack(side=tk.LEFT)

        def select_folder(folder_path, Event=None):
            folder_path.set(filedialog.askdirectory(initialdir=os.curdir))

        def entry_template(frame, label):
            entry_frame = tk.Frame(frame)
            entry_frame.pack(side=tk.TOP, fill=tk.X)
            tk.Label(entry_frame, text=label, width=len("Destination folder:"), anchor=tk.W).pack(side=tk.LEFT)
            filepath = tk.StringVar()
            entry_path = tk.Entry(entry_frame, textvariable=filepath, width=60, exportselection=0)
            entry_path.pack(side=tk.LEFT)
            tk.Button(
                entry_frame, text="...", command=lambda: (select_folder(filepath))
            ).pack(side=tk.LEFT)
            return entry_frame

        self.frame_batch_source_path = entry_template(self.frame_batch_tools, "Source folder:")
        self.frame_batch_source_path = entry_template(self.frame_batch_tools, "Destination folder:")


    def toggle_tool_view(self, Event=None):
        if self.tool_view.get() is VIEW_IMG_TOOL:
            self.frame_batch_tools.pack_forget()
            self.frame_img_tools.pack(side=tk.TOP, fill=tk.BOTH)
        elif self.tool_view.get() is VIEW_BATCH_EDIT_TOOL:
            self.frame_img_tools.pack_forget()
            self.frame_batch_tools.pack(side=tk.TOP, fill=tk.BOTH)

    def adjust_brightness(self, value: float):
        self.refresh_workspace()

    def adjust_contrast(self, value: float):
        self.refresh_workspace()

    def save(self, Event=None):
        filename = filedialog.asksaveasfilename(
            initialdir=os.curdir, filetypes=SAVE_FILETYPES
        )
        self.img_workspace.save(filename)

    def process_img(self, chan: Image, color):
        img = ImageOps.colorize(chan, (0, 0, 0), color).convert("RGBA")
        # mask = chan.point(lambda i: i < 50 and 255)
        enhancer_contrast = ImageEnhance.Contrast(img)
        img = enhancer_contrast.enhance(self.contrast_slider.get() / 100)
        enhancer_brightness = ImageEnhance.Brightness(img)
        img = enhancer_brightness.enhance(self.brightness_slider.get() / 100)
        return img

    def refresh_workspace(self):
        self.img_workspace = self.img_og_dif.copy()
        for idx, chan in enumerate(self.tem_channels):
            color = ImageColor.getrgb(self.color_boxes[idx]["bg"])
            if color != (128, 128, 128):
                chan.convert("L")
                processed_img = self.process_img(chan, color)
                self.img_workspace = ImageChops.add(self.img_workspace, processed_img)
        self.img_dif = ImageTk.PhotoImage(self.img_workspace)
        self.label_img_dif.config(image=self.img_dif)

    def refresh_window_size(self, Event=None):
        img_dif_size = self.img_workspace.size
        img_tem_size = self.img_og_tem.size
        new_width = img_dif_size[0] + img_tem_size[0]
        # Assuming both image got same size
        new_height = img_dif_size[1] + FRAME_TOOL_HEIGHT
        self.geometry(f"{new_width}x{new_height}")

    def apply_color(self, btn_idx: int):
        _, color = self.color_dialog.show()
        if color is not None:
            self.color_boxes[btn_idx]["bg"] = color
            self.draw_rgb_value()
        self.refresh_workspace()

    def apply_alpha(self):
        for i in self.lb.curselection():
            alpha_mask = ImageChops.invert(self.tem_channels[i])
            self.img_workspace.putalpha(alpha_mask)

    def select_channel(self, Event=None):
        new_img = Image.new("L", self.img_og_tem.size)
        for i in self.lb.curselection():
            # TODO: think about clean implementation
            try:
                new_img = ImageChops.add(new_img, self.tem_channels[i])
            except IndexError:
                return
        self.img = ImageTk.PhotoImage(new_img)
        self.label_img_tem.config(image=self.img)

    def load_file(self, filename: str):
        # IMG LOADER
        # Diffuse image
        self.img_og_dif = Image.open(filename)
        background = Image.new("RGBA", self.img_og_dif.size, (0, 0, 0))
        self.img_og_dif = Image.alpha_composite(background, self.img_og_dif)

        # Load associated tem file
        tem_filename = filename.replace("_dif.", "_tem.")
        self.load_channel_packed_file(tem_filename)
        self.refresh_workspace()
        self.refresh_window_size()

    def load_channel_packed_file(self, filename: str):
        # tem image
        self.img_og_tem = Image.open(filename)
        self.img_tem = ImageTk.PhotoImage(self.img_og_tem)
        self.tem_channels = self.img_og_tem.split()
        self.select_channel()

    def open_diffuse(self, Event=None):
        f = filedialog.askopenfile(initialdir=os.curdir, filetypes=OPEN_FILETYPES)
        self.load_file(f.name)

    def open_channel(self, Event=None):
        with filedialog.askopenfile(
            initialdir=os.curdir, filetypes=OPEN_FILETYPES
        ) as f:
            self.load_channel_packed_file(f.name)

    def batch_edit(self, Event=None):
        source = filedialog.askdirectory(initialdir=os.curdir)
        dest = filedialog.askdirectory(initialdir=os.curdir)
        for filename in os.listdir(source):
            if filename.endswith("_dif.dds"):
                self.load_file(f"{source}/{filename}")
                tga_filename = filename[:-4] + ".tga"
                self.img_workspace.save(f"{dest}/{tga_filename}")

    def reset_workspace(self, Event=None):
        self.img_workspace = self.img_og_dif
        for color_box in self.color_boxes:
            color_box["bg"] = "gray"
        self.brightness_slider.set(40)
        self.contrast_slider.set(100)
        self.lb.selection_set(first=0, last=3)
        self.select_channel()
        self.refresh_workspace()

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


if __name__ == "__main__":
    army_painter = ArmyPainter()
    army_painter.mainloop()
