import tkinter as tk
from army_color import army_color_preset

class FramePatternList(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super(FramePatternList, self).__init__(master=master, cnf={}, **kw)
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lb = tk.Listbox(self, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lb.yview)

        for idx, pattern_name in enumerate(army_color_preset):
            self.lb.insert(idx, pattern_name)
        self.lb.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.save_pattern = tk.Button(
            self, text="Save pattern", command=self._root().save_pattern
        )
        self.save_pattern.pack(side=tk.TOP, fill=tk.X)
