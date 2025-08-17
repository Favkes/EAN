import tkinter as tk


class IntervalGUI(tk.Frame):
    def __init__(self, root_frame: tk.Frame):
        super().__init__(root_frame)
        self.root_frame = root_frame

        self.label = tk.Label(self, text="INTERVAL")
        self.label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root)
    gui = IntervalGUI(frame)
    frame.pack()
    gui.pack()
    root.mainloop()

