import tkinter as tk


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

        # Offset slider
        self.offset_slider = tk.Scale(
            self,
            label="Offset",
            length=200,
            from_=-100.0,
            to=100.0,
            orient=tk.HORIZONTAL,
            command=self._root().on_slider_update,
        )
        self.offset_slider.pack(side=tk.TOP, fill=tk.X)
