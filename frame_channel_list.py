import tkinter as tk


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
        self.add_alpha = tk.Button(
            self, text="Apply alpha", height=2, command=self._root().apply_alpha
        )
        self.add_alpha.pack(side=tk.TOP, fill=tk.X)
