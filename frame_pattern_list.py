import tkinter as tk
from color_pattern_handler import army_color_pattern

class FramePatternList(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super(FramePatternList, self).__init__(master=master, cnf={}, **kw)
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lb = tk.Listbox(self, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set)
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
        self.lb.delete(0, 'end')
        for idx, pattern_name in enumerate(army_color_pattern):
            self.lb.insert(idx, pattern_name)
        self.lb.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
