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
            command=self._root().adjust_brightness,
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
            command=self._root().adjust_contrast,
        )
        self.contrast_slider.pack(side=tk.TOP, fill=tk.X)
