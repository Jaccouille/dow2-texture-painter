import os
import tkinter as tk
from tkinter import colorchooser
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


def create_placeholder_img():
    img = Image.new("RGBA", (256, 256))
    d1 = ImageDraw.Draw(img)
    d1.text(xy=(128, 128), fill="black", text="Diffuse PlaceHolder")
    return img


class ArmyPainter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x1000")
        self.title("Army Painter")
        self.tem_channels = []

        # Frame IMG
        self.frame_img = tk.Frame(self)
        self.frame_img.pack(side=tk.BOTTOM)

        # Frame TEXT
        self.frame_tools = tk.Frame(self, width=1000, height=300)
        self.frame_tools.place(anchor=tk.NW)

        self.img_og_dif = create_placeholder_img()
        self.img_dif = ImageTk.PhotoImage(self.img_og_dif)

        # Label SETTING DIF
        self.label_img_dif = tk.Label(self.frame_img, image=self.img_dif)
        self.label_img_dif.pack(side=tk.LEFT)

        self.img_og_tem = create_placeholder_img()
        self.img_tem = ImageTk.PhotoImage(self.img_og_tem)
        # LABEL SETTING TEM
        self.label_img_tem = tk.Label(self.frame_img, image=self.img_tem)
        self.label_img_tem.pack(side=tk.RIGHT)

        # Channel List Frame
        self.frame_channel_list = tk.LabelFrame(self.frame_tools, text="Channel List", relief=tk.GROOVE)
        self.frame_channel_list.pack(side=tk.RIGHT, fill=tk.Y)

        # Channel List Box
        self.lb = tk.Listbox(self.frame_channel_list, selectmode=tk.MULTIPLE, height=4, width=9)
        self.lb.insert(0, "0 Red")
        self.lb.insert(1, "1 Green")
        self.lb.insert(2, "2 Blue")
        self.lb.insert(3, "3 Alpha")
        self.bind("<<ListboxSelect>>", self.select_channel)
        self.lb.pack(side=tk.TOP, fill=tk.X)

        # Add alpha BTN
        self.add_alpha = tk.Button(
            self.frame_channel_list, text="Apply alpha", command=self.apply_alpha
        )
        self.add_alpha.pack(side=tk.LEFT, fill=tk.X)

        # Color Dialog that open upon btn click
        self.color_dialog = colorchooser.Chooser(self)

        # Color boxes
        self.frame_boxes = tk.Frame(
            self.frame_tools,
            relief=tk.SOLID,
            width=COLOR_BOX_SIZE * 4 + 5,
            height=COLOR_BTN_HEIGHT + COLOR_BOX_SIZE,
        )
        # self.frame_boxes.place(anchor=tk.NW)
        self.frame_boxes.pack(side=tk.TOP)

        self.color_boxes = []
        self.color_buttons = []
        for i in range(0, 4):
            self.color_boxes.append(
                tk.Canvas(
                    self.frame_boxes,
                    bg="gray",
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
                    relief=tk.RIDGE,
                    command=partial(self.apply_color, i),
                )
            )
            self.color_buttons[i].place(anchor=tk.NW, x=COLOR_BOX_SIZE * i, y=0)

        # # Brightness slider
        # self.brightness_slider = tk.Scale(
        #     self.frame_tools,
        #     from_=0.0,
        #     to=150.0,
        #     orient=tk.HORIZONTAL,
        #     command=self.adjust_brightness,
        # )
        # self.brightness_slider.pack()

        # # Contrast slider
        # self.contrast_slider = tk.Scale(
        #     self.frame_tools,
        #     from_=0.0,
        #     to=200.0,
        #     orient=tk.HORIZONTAL,
        #     command=self.adjust_contrast,
        # )
        # self.contrast_slider.pack()
        # self.reset_workspace()

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(
            label="Open diffuse", command=self.open_diffuse, accelerator="Ctrl+O"
        )
        filemenu.add_command(
            label="Open channel file", command=self.open_channel, accelerator="Ctrl+C"
        )
        filemenu.add_command(label="Save", command=self.save, accelerator="Ctrl+S")
        filemenu.add_command(
            label="Batch Edit", command=self.batch_edit, accelerator="Ctrl+D"
        )
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(
            label="Reset workspace", command=self.reset_workspace, accelerator="Ctrl+R"
        )
        menubar.add_cascade(label="Edit", menu=editmenu)

        self.bind("<Control-o>", self.open_diffuse)
        self.bind("<Control-c>", self.open_channel)
        self.bind("<Control-s>", self.save)
        self.bind("<Control-d>", self.batch_edit)
        self.bind("<Control-r>", self.reset_workspace)
        self.draw_rgb_value()

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
                tga_filename = filename[:-3] + ".tga"
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
