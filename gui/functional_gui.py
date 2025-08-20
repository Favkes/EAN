import tkinter as tk


class InputGUI(tk.Frame):
    def __init__(self, root_frame: tk.Frame):
        super().__init__(root_frame)
        self.root_frame = root_frame
        self.config(
            padx=15
        )

        self.input_field_title = tk.Label(
            self,
            text="Input data:"
        )
        self.input_field_entry = tk.Text(
            self,
            height=5,
            width=20
        )

    def build(self):
        self.input_field_title.grid(
            row=0, column=0, sticky='w'
        )
        self.input_field_entry.grid(
            row=1, column=0, sticky='w'
        )


if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root)
    gui = InputGUI(frame)
    frame.pack()
    gui.pack()
    root.mainloop()
