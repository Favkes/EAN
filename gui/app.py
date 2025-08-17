import tkinter as tk


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("700x500")
        self.root.minsize(400, 300)
        self.root.maxsize(800, 600)
        self.root.config(
            padx=5, pady=5
        )

        self.mainframe = None

    def build(self):
        self.mainframe = tk.Frame(self.root)



    def display(self):
        self.mainframe.pack()
        self.root.mainloop()


