import os
import tkinter as tk
from tkinter import colorchooser
from PIL import (
    Image,
    ImageChops,
    ImageOps,
    ImageTk,
    ImageColor,
    ImageEnhance,
    ImageDraw,
)
from functools import partial
from tkinter import filedialog
from frame_color_box import FrameColorChooser
from frame_channel_list import FrameChannelList
from frame_slider import FrameSlider
from frame_batch_tool import FrameBatchTool
from constant import *

VIEW_IMG_TOOL = 0
VIEW_BATCH_EDIT_TOOL = 1

path = os.path.dirname(__file__)


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

        # Setting main window
        min_width = 678
        min_height = DEFAULT_IMG_SIZE + FRAME_TOOL_HEIGHT
        dimension = f"{min_width}x{min_height}"
        self.geometry(dimension)
        self.minsize(min_width, min_height)
        self.title("Army Painter")

        # RGBA channel of tem texture file
        self.tem_channels = []

        # Frame containing tools to edit the image
        self.frame_img_tools = tk.Frame(
            self,
            width=DEFAULT_IMG_SIZE * 2,
            height=COLOR_BOX_SIZE + COLOR_BTN_HEIGHT,
            bd=2,
            relief=tk.RIDGE,
        )
        self.frame_img_tools.pack(side=tk.TOP, fill=tk.BOTH)

        # Defining slave widget
        self.define_frame_img_tool()

        # Frame containing the texture images
        self.frame_img = tk.Frame(self)
        self.frame_img.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        # Defining slave widget
        self.define_frame_img()

        # Frame containing the batch operation tools
        self.frame_batch_tools = FrameBatchTool(
            self,
            width=DEFAULT_IMG_SIZE * 2,
            height=COLOR_BOX_SIZE + COLOR_BTN_HEIGHT,
            bd=2,
            relief=tk.RIDGE,
        )
        self.frame_batch_tools.pack_forget()

        # Defining slave widget
        # self.define_frame_batch_tool()

        # Defining menubar
        self.define_menu()

        # Initialize the default workspace
        self.reset_workspace()

    def define_frame_img_tool(self):
        # Setting color boxes frame
        self.frame_color_chooser = FrameColorChooser(
            self.frame_img_tools,
            width=COLOR_BOX_SIZE * 4 + 12,
            height=COLOR_BOX_SIZE + COLOR_BTN_HEIGHT,
            bd=0,
            relief=tk.RIDGE,
        )
        self.frame_color_chooser.pack(side=tk.LEFT, fill=tk.Y)

        # Setting channel list frame
        self.frame_channel_select = FrameChannelList(
            self.frame_img_tools, text="RGBA Channel", relief=tk.RIDGE, bd=2
        )
        self.bind("<<ListboxSelect>>", self.select_channel)
        self.frame_channel_select.pack(side=tk.LEFT, fill=tk.Y)

        # Setting sliders
        self.frame_sliders = FrameSlider(self.frame_img_tools, relief=tk.RIDGE, bd=2)
        self.frame_sliders.pack(side=tk.LEFT, fill=tk.Y)

    def define_menu(self):
        menubar = tk.Menu(self)

        def define_filemenu():
            filemenu = tk.Menu(menubar, tearoff=0)
            filemenu.add_command(
                label="Open diffuse", command=self.open_diffuse, accelerator="Ctrl+O"
            )
            filemenu.add_command(
                label="Open channel file",
                command=self.open_channel,
                accelerator="Ctrl+A",
            )
            filemenu.add_command(label="Save", command=self.save, accelerator="Ctrl+S")
            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=self.quit)
            menubar.add_cascade(label="File", menu=filemenu)
            self.config(menu=menubar)

        def define_editmenu():
            editmenu = tk.Menu(menubar, tearoff=0)
            editmenu.add_command(
                label="Reset workspace",
                command=self.reset_workspace,
                accelerator="Ctrl+R",
            )
            menubar.add_cascade(label="Edit", menu=editmenu)

        def define_toolmenu():
            self.tool_view = tk.IntVar()
            toolmenu = tk.Menu(menubar, tearoff=0)
            toolmenu.add_radiobutton(
                label="Image Tools",
                variable=self.tool_view,
                value=VIEW_IMG_TOOL,
                command=self.toggle_tool_view,
            )
            toolmenu.add_radiobutton(
                label="Batch Edit Tools",
                variable=self.tool_view,
                value=VIEW_BATCH_EDIT_TOOL,
                command=self.toggle_tool_view,
            )
            menubar.add_cascade(label="Tools", menu=toolmenu)

        define_editmenu()
        define_filemenu()
        define_toolmenu()

        # Define Menu binding
        self.bind("<Control-o>", self.open_diffuse)
        self.bind("<Control-a>", self.open_channel)
        self.bind("<Control-s>", self.save)
        self.bind("<Control-d>", self.batch_edit)
        self.bind("<Control-r>", self.reset_workspace)

    def define_frame_img(self):
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

    def toggle_tool_view(self, Event=None):
        if self.tool_view.get() is VIEW_IMG_TOOL:
            self.frame_batch_tools.pack_forget()
            self.frame_img_tools.pack(side=tk.TOP, fill=tk.BOTH)
        elif self.tool_view.get() is VIEW_BATCH_EDIT_TOOL:
            self.frame_img_tools.pack_forget()
            self.frame_batch_tools.pack(side=tk.TOP, fill=tk.BOTH)

    def set_brightness(self, value: float):
        self.refresh_workspace()

    def set_contrast(self, value: float):
        self.refresh_workspace()

    def save(self, Event=None):
        """Save image from current workspace

        :param Event: widget triggered event, defaults to None
        :type Event: [type], optional
        """
        filename = filedialog.asksaveasfilename(
            initialdir=os.curdir, filetypes=SAVE_FILETYPES
        )
        self.img_workspace.save(filename)

    def process_img(self, channel: Image, color: tuple):
        """Process image with current workspace setting

        :param channel: channel data selected from the tem file, used as a layer
        to colorize the image
        :type channel: Image
        :param color: RGBA Color used to colorize the image
        :type color: tuple
        :return: Processed Image
        :rtype: Image
        """
        img = ImageOps.colorize(channel, (0, 0, 0), color).convert("RGBA")
        enhancer_contrast = ImageEnhance.Contrast(img)
        img = enhancer_contrast.enhance(self.frame_sliders.contrast_slider.get() / 100)
        enhancer_brightness = ImageEnhance.Brightness(img)
        img = enhancer_brightness.enhance(
            self.frame_sliders.brightness_slider.get() / 100
        )
        return img

    def refresh_workspace(self):
        """Refresh the workspace image with current settings"""
        self.img_workspace = self.img_og_dif.copy()
        for idx, channel in enumerate(self.tem_channels):
            color = ImageColor.getrgb(self.frame_color_chooser.color_boxes[idx]["bg"])
            if color != (128, 128, 128):
                channel.convert("L")
                processed_img = self.process_img(channel, color)
                self.img_workspace = ImageChops.add(self.img_workspace, processed_img)
        self.img_dif = ImageTk.PhotoImage(self.img_workspace)
        self.label_img_dif.config(image=self.img_dif)

    def refresh_window_size(self):
        """Refresh window size using current images width"""
        img_dif_size = self.img_workspace.size
        img_tem_size = self.img_og_tem.size
        new_width = img_dif_size[0] + img_tem_size[0]

        # Assuming both image got same size
        new_height = img_dif_size[1] + FRAME_TOOL_HEIGHT
        self.geometry(f"{new_width}x{new_height}")
        self.update()

    def apply_alpha(self):
        """Takes selected channel layer and apply alpha on the workspace image"""
        for i in self.frame_channel_select.lb.curselection():
            alpha_mask = ImageChops.invert(self.tem_channels[i])
            self.img_workspace.putalpha(alpha_mask)

    def select_channel(self, Event=None):
        """Register channel selected from the Channel list listbox

        :param Event: event triggered from widget, defaults to None
        :type Event: [type], optional
        """
        new_img = Image.new("L", self.img_og_tem.size)
        for i in self.frame_channel_select.lb.curselection():
            # TODO: think about clean implementation
            try:
                new_img = ImageChops.add(new_img, self.tem_channels[i])
            except IndexError:
                return
        self.img = ImageTk.PhotoImage(new_img)
        self.label_img_tem.config(image=self.img)

    def load_file(self, filepath: str):
        """Load diffuse and tem texture and set it as workspace image,
        both texture have to be located in the same directory

        :param filepath: path to file
        :type filepath: str
        """
        # IMG LOADER
        # Diffuse image
        self.img_og_dif = Image.open(filepath)
        background = Image.new("RGBA", self.img_og_dif.size, (0, 0, 0))
        self.img_og_dif = Image.alpha_composite(background, self.img_og_dif)

        # Load associated tem file
        if self.frame_batch_tools.dif_pattern.get() != "" and self.frame_batch_tools.tem_pattern.get() != "":
            tem_filepath = filepath.replace(self.frame_batch_tools.dif_pattern.get(), self.frame_batch_tools.tem_pattern.get())
        else:
            tem_filepath = filepath.replace("_dif.", "_tem.")
        self.load_channel_packed_file(tem_filepath)
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
        source = self.frame_batch_tools.frame_batch_source_path.folder_path.get()
        dest = self.frame_batch_tools.frame_batch_destination_path.folder_path.get()
        dest_format = self.frame_batch_tools.dest_format.get().lower()
        dif_file_pattern = self.frame_batch_tools.dif_pattern.get()
        for filename in os.listdir(source):
            name, ext = os.path.splitext(filename)
            if ext[1:] in OPEN_EXT_LIST and name.endswith(dif_file_pattern):
                self.load_file(f"{source}/{filename}")
                new_filename = name + f".{dest_format}"
                self.img_workspace.save(f"{dest}/{new_filename}")

    def reset_workspace(self, Event=None):
        self.img_workspace = self.img_og_dif
        for color_box in self.frame_color_chooser.color_boxes:
            color_box["bg"] = "gray"
        self.frame_sliders.brightness_slider.set(40)
        self.frame_sliders.contrast_slider.set(100)
        self.frame_channel_select.lb.selection_set(first=0, last=3)
        self.select_channel()
        self.refresh_workspace()


if __name__ == "__main__":
    army_painter = ArmyPainter()
    army_painter.mainloop()
