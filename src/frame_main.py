import os
from PIL import (
    ImageTk,
)
import tkinter as tk
from tkinter import filedialog
from tkinter.simpledialog import askstring
from tkinter.messagebox import showerror
import traceback
from src.widget import (
    FrameColorChooser,
    FrameChannelList,
    FrameColorOps,
    FrameSlider,
    BatchEditTopLevel,
    FramePatternList,
)
from src.constant import (
    DEFAULT_IMG_SIZE,
    COLOR_BOX_SIZE,
    COLOR_BTN_HEIGHT,
    FRAME_TOOL_HEIGHT,
    SAVE_FILETYPES,
    OPEN_FILETYPES,
    OPEN_EXT_LIST,
)
import src.color_pattern_handler
from src.color_pattern_handler import army_color_pattern
from src.image_process import ImageWorkbench
from pathlib import Path

from importlib import resources

PATTERN_LIST_DEFAULT_WIDTH = 166
VERSION = "0.1"

class ArmyPainter(tk.Tk):
    def __init__(self):
        super().__init__()

        # Setting main window
        min_width = 256 * 2 + PATTERN_LIST_DEFAULT_WIDTH
        min_height = DEFAULT_IMG_SIZE + FRAME_TOOL_HEIGHT
        dimension = f"{min_width}x{min_height}"
        self.geometry(dimension)
        with resources.path("resources", "icon_64x64.png") as icon_path:
            self.icon_img = tk.PhotoImage(file=icon_path)
        self.iconphoto(False, self.icon_img)
        self.minsize(min_width, min_height)
        self.title(f"Army Painter {VERSION}")

        self.img_wbench = ImageWorkbench()

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
        self.define_frame_workspace_tool()

        # Frame containing the texture images
        self.frame_img = tk.Frame(self)
        self.frame_img.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        # Defining slave widget
        self.define_frame_workspace()
        self.frame_army_pattern = FramePatternList(self.frame_img)
        self.frame_army_pattern.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.bind("<<ListboxSelect>>", self.on_listbox_select)

        # Defining menubar
        self.define_menu()

        # Initialize the default workspace
        self.reset_workspace()

    def define_frame_workspace_tool(self):
        # Setting color boxes frame
        self.frame_color_chooser = FrameColorChooser(
            self.frame_img_tools,
            width=COLOR_BOX_SIZE * 4 + 12,
            height=COLOR_BOX_SIZE + COLOR_BTN_HEIGHT,
            bd=0,
            relief=tk.RIDGE,
        )
        self.frame_color_chooser.pack(side=tk.LEFT, fill=tk.Y)

        self.frame_color_op_option = FrameColorOps(
            self.frame_img_tools,
            text="Color Operation",
        )
        self.frame_color_op_option.pack(side=tk.TOP, fill=tk.X)

        # Setting channel list frame
        self.frame_channel_select = FrameChannelList(
            self.frame_img_tools, text="RGBA Channel", relief=tk.RIDGE, bd=2
        )
        self.frame_channel_select.pack(side=tk.LEFT, fill=tk.Y)

        # Setting sliders
        self.frame_sliders = FrameSlider(
            self.frame_img_tools, relief=tk.RIDGE, bd=2
        )
        self.frame_sliders.pack(side=tk.LEFT, fill=tk.Y)

    def define_menu(self):
        menubar = tk.Menu(self)

        def define_filemenu():
            filemenu = tk.Menu(menubar, tearoff=0)
            filemenu.add_command(
                label="Open diffuse",
                command=self.open_diffuse,
                accelerator="Ctrl+O",
            )
            filemenu.add_command(
                label="Open channel file",
                command=self.open_channel,
                accelerator="Ctrl+A",
            )
            filemenu.add_command(
                label="Save as", command=self.save, accelerator="Ctrl+S"
            )
            filemenu.add_command(
                label="Close", command=self.close, accelerator="Ctrl+E"
            )
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
            self.apply_dirt = tk.BooleanVar()
            editmenu.add_checkbutton(
                label="Apply Dirt Texture",
                variable=self.apply_dirt,
                onvalue=1,
                offvalue=0,
                command=self.on_dirt_toggle,
            )
            self.apply_spec = tk.BooleanVar()
            editmenu.add_checkbutton(
                label="Apply Specular Texture",
                variable=self.apply_spec,
                onvalue=1,
                offvalue=0,
                command=self.on_spec_toggle,
            )
            menubar.add_cascade(label="Edit", menu=editmenu)

        def define_toolmenu():
            toolmenu = tk.Menu(menubar, tearoff=0)
            toolmenu.add_command(
                label="Batch Edit Tools",
                command=self.open_batch_edit_tools,
            )
            menubar.add_cascade(label="Tools", menu=toolmenu)

        define_filemenu()
        define_editmenu()
        define_toolmenu()

        # Define Menu binding
        self.bind("<Control-o>", self.open_diffuse)
        self.bind("<Control-a>", self.open_channel)
        self.bind("<Control-s>", self.save)
        self.bind("<Control-e>", self.close)
        self.bind("<Control-d>", self.batch_edit)
        self.bind("<Control-r>", self.reset_workspace)

    def define_frame_workspace(self):
        self.img_dif = ImageTk.PhotoImage(self.img_wbench.img_og_dif)
        self.label_img_dif = tk.Label(
            self.frame_img, image=self.img_dif, relief=tk.RAISED
        )
        self.label_img_dif.pack(side=tk.LEFT, fill=tk.Y)

        self.img_tem = ImageTk.PhotoImage(self.img_wbench.img_og_tem)
        self.label_img_tem = tk.Label(
            self.frame_img, image=self.img_tem, relief=tk.RAISED
        )
        self.label_img_tem.pack(side=tk.LEFT, fill=tk.Y)

    def open_batch_edit_tools(self, Event=None):
        # Frame containing the batch operation tools
        self.frame_batch_tools = BatchEditTopLevel(
            self,
            width=DEFAULT_IMG_SIZE * 2,
            height=COLOR_BOX_SIZE + COLOR_BTN_HEIGHT,
            bd=2,
            relief=tk.RIDGE,
        )
        self.frame_batch_tools.iconphoto(
            False, self.icon_img
        )

    def on_slider_update(self, value: float):
        self.img_wbench.brightness = self.frame_sliders.brightness_slider.get()
        self.img_wbench.contrast = self.frame_sliders.contrast_slider.get()
        self.refresh_workspace()

    def save(self, Event=None):
        """Save image from current workspace

        :param Event: widget triggered event, defaults to None
        :type Event: [type], optional
        """
        filename = filedialog.asksaveasfilename(
            initialdir=os.curdir,
            filetypes=SAVE_FILETYPES,
            defaultextension=SAVE_FILETYPES[0],
            initialfile=self.og_filename,
        )
        if filename:
            try:
                self.img_wbench.save(filename)
            except KeyError as error:
                tk.messagebox.showerror(
                    title="Wrong File Extension",
                    message='Error: wrong extension, choose an extension from the "Save as type" list',
                )

    def close(self, Event=None):
        self.img_wbench.set_placeholder_img()
        self.img_wbench.tem_channels = []
        self.refresh_workspace()

    def refresh_workspace(self):
        """Refresh the workspace image with current settings"""
        self.img_wbench.colors = [
            color["bg"] for color in self.frame_color_chooser.color_boxes
        ]
        self.img_dif = ImageTk.PhotoImage(self.img_wbench.refresh_workspace())
        self.label_img_dif.config(image=self.img_dif)
        self.img_tem = ImageTk.PhotoImage(
            self.img_wbench.refresh_team_colour_img()
        )
        self.label_img_tem.config(image=self.img_tem)
        self.refresh_window_size()

    def color_operation_update(self):
        color_op = self.frame_color_op_option.var.get()
        self.img_wbench.color_op = color_op
        self.refresh_workspace()

    def on_apply_alpha_toggle(self):
        self.img_wbench.apply_alpha = (
            self.frame_channel_select.apply_alpha.get()
        )
        self.refresh_workspace()

    def on_dirt_toggle(self):
        self.img_wbench.apply_dirt = self.apply_dirt.get()
        self.refresh_workspace()

    def on_spec_toggle(self):
        self.img_wbench.apply_spec = self.apply_spec.get()
        self.refresh_workspace()

    def refresh_window_size(self):
        """Refresh window size using current images width"""
        img_dif_size = self.img_wbench.img_workspace.size
        img_tem_size = self.img_wbench.img_og_tem.size
        new_width = (
            img_dif_size[0] + img_tem_size[0] + PATTERN_LIST_DEFAULT_WIDTH
        )

        # Assuming both image got same size
        new_height = img_dif_size[1] + FRAME_TOOL_HEIGHT
        self.geometry(f"{new_width}x{new_height}")
        self.update()

    def on_listbox_select(self, Event=None):
        if type(Event.widget.master) is FrameChannelList:
            self.select_channel()
        # TODO: Refactor following code so with frame color class
        elif type(Event.widget.master) is FramePatternList:
            # TODO: This function is triggered upon listbox selection set.
            # Is this intended? This cause issue with the reset_workspace function
            # triggering the event when the pattern listbox has no selection
            if len(self.frame_army_pattern.lb.curselection()) == 0:
                return
            idx = self.frame_army_pattern.lb.curselection()[0]
            army_name = self.frame_army_pattern.lb.get(idx)
            color_list = list(army_color_pattern.get(army_name).values())
            for color, color_box in zip(
                color_list, self.frame_color_chooser.color_boxes
            ):
                color_box["bg"] = color
            self.frame_color_chooser.draw_rgb_value()
            self.refresh_workspace()

    def select_channel(self, Event=None):
        """Register channel selected from the Channel list listbox

        :param Event: event triggered from widget, defaults to None
        :type Event: [type], optional
        """
        self.img_wbench.tem_selected = (
            self.frame_channel_select.lb.curselection()
        )
        # TODO: refactor lazy check with is load batch
        # Did to avoid exception in ImageWorkbench processing
        if self.img_wbench.apply_alpha:
            self.refresh_workspace()
        self.img = ImageTk.PhotoImage(
            self.img_wbench.refresh_team_colour_img()
        )
        self.label_img_tem.config(image=self.img)

    def load_file(self, filepath: str):
        """Load diffuse and tem texture and set it as workspace image,
        both texture have to be located in the same directory

        :param filepath: path to file
        :type filepath: str
        """
        self.img_wbench.load_diffuse_file(filepath)

        # Load associated tem file
        tem_filepath = filepath.replace("_dif.", "_tem.")
        if os.path.isfile(tem_filepath):
            self.load_channel_packed_file(tem_filepath)
        else:
            self.open_channel()

        # Load associated dirt file
        dirt_filepath = filepath.replace("_dif.", "_drt.")
        if os.path.isfile(dirt_filepath):
            self.load_dirt_file(dirt_filepath)

        # Load associated spec file
        spec_filepath = filepath.replace("_dif.", "_spc.")
        if os.path.isfile(spec_filepath):
            self.load_spec_file(spec_filepath)

        self.refresh_workspace()

    def load_channel_packed_file(self, filepath: str):
        self.img_wbench.load_team_colour_file(filepath)
        self.img_tem = ImageTk.PhotoImage(self.img_wbench.img_og_tem)
        self.select_channel()

    def load_dirt_file(self, filepath: str):
        self.img_wbench.load_dirt_file(filepath)

    def load_spec_file(self, filepath: str):
        self.img_wbench.load_specular_file(filepath)

    def open_diffuse(self, Event=None):
        f = filedialog.askopenfile(
            initialdir=os.curdir, filetypes=OPEN_FILETYPES
        )
        if f is None:
            return
        # Saving the filename just to set it as default file name on the save
        # file dialog, truncate the file extension because it is automatically set
        # by the save dialog
        self.og_filename = Path(f.name).name.split(".")[0]
        self.load_file(f.name)

    def open_channel(self, Event=None):
        f = filedialog.askopenfile(
            initialdir=os.curdir,
            filetypes=OPEN_FILETYPES,
            title="Open channel file",
        )
        if f is None:
            return
        self.load_file(f.name)

    def _check_batch_path(self, source: str, dest: str):
        if source == "":
            raise OSError("Please select a source directory.")
        elif dest == "":
            raise OSError("Please select a destination directory.")
        elif not os.path.exists(source):
            raise OSError(f"{source} does not exist.")
        elif not os.path.exists(dest):
            raise OSError(f"{dest} does not exist.")

    def _check_dif_format(self, filename: str, src_format: list):
        name, ext = os.path.splitext(filename)
        if ext[1:] in src_format and name.endswith("_dif"):
            return True
        return False

    def batch_edit(self, Event=None):
        source = self.frame_batch_tools.frame_batch_src_path.entry_value.get()
        dest = self.frame_batch_tools.frame_batch_dest_path.entry_value.get()
        dest_format = self.frame_batch_tools.dest_format.get().lower()

        try:
            # Checking if source & dest exist
            self._check_batch_path(source, dest)

            src_format = self.frame_batch_tools.get_source_format_selected()
            filenames = [
                filename
                for filename in os.listdir(source)
                if self._check_dif_format(filename, src_format)
            ]

            self.frame_batch_tools.progress_bar["maximum"] = len(filenames)
            for idx, filename in enumerate(filenames):
                name, _ = os.path.splitext(filename)
                self.load_file(f"{source}/{filename}")
                new_filename = name + f".{dest_format}"
                self.img_wbench.save(f"{dest}/{new_filename}")
                self.frame_batch_tools.update_progress_bar_label(idx + 1)
        except OSError as e:
            showerror(title="Path Error", message=str(e))
        finally:
            self.frame_batch_tools.focus()

    def reset_workspace(self, Event=None):
        self.img_wbench.img_workspace = self.img_wbench.img_og_dif
        for color_box in self.frame_color_chooser.color_boxes:
            color_box["bg"] = "#808080"
        self.frame_sliders.brightness_slider.set(40)
        self.frame_sliders.contrast_slider.set(100)
        self.frame_channel_select.lb.selection_set(first=0, last=3)
        self.select_channel()
        self.refresh_workspace()

    def save_pattern(self):
        pattern_name = askstring("Pattern Name", "Choose a pattern name")
        colors = [
            color["bg"] for color in self.frame_color_chooser.color_boxes
        ]
        src.color_pattern_handler.save(name=pattern_name, colors=colors)
        self.frame_army_pattern.load_pattern_list()
        self.frame_army_pattern.lb.selection_set(first="end", last="end")
        self.frame_army_pattern.lb.yview_moveto(fraction=1)

    def delete_pattern(self):
        idx = self.frame_army_pattern.lb.curselection()[0]
        pattern_name = self.frame_army_pattern.lb.get(idx)
        src.color_pattern_handler.delete(pattern_name)
        self.frame_army_pattern.load_pattern_list()
        self.reset_workspace()

    def report_callback_exception(self, exc, val, tb):
        showerror("Error", message=traceback.format_exc())


def main():
    army_painter = ArmyPainter()
    army_painter.mainloop()


if __name__ == "__main__":
    main()
