import tkinter as tk
from utility import entry_bindings


class InputGUI(tk.Frame):
    def __init__(self,
                 app_core,
                 root_frame: tk.Frame,
                 title: str = 'Input data:',
                 dims: tuple[int, int] = (20, 5)):
        super().__init__(root_frame)
        self.root_frame = root_frame
        self.config(
            padx=15
        )

        self.app_core = app_core

        self.input_field_title = tk.Label(
            self,
            text=title
        )
        self.input_field_entry = tk.Text(
            self,
            height=dims[1],
            width=dims[0],
        )

        self.input_field_entry_placeholder = ''
        self.input_field_entry_allowed_chars = '0.123,456;789\n'

        self.input_field_entry.bind(
            "<FocusIn>",
            self.input_field_entry_clear_hint
        )
        self.input_field_entry.bind(
            "<FocusOut>",
            lambda event: entry_bindings.focus_out(
                self.input_field_entry,
                hint_text=self.input_field_entry_placeholder,
                event=event
            )
        )

        self.update_input_filter()


    def input_field_entry_clear_hint(self, event):
        return entry_bindings.clear_hint(
            self.input_field_entry,
            hint_text=self.input_field_entry_placeholder,
            event=event
        )


    def update_input_filter(self, allowed_chars: str = None):
        if allowed_chars is None:
            allowed_chars = self.input_field_entry_allowed_chars
        else:
            self.input_field_entry_allowed_chars = allowed_chars

        content = self.input_field_entry.get("1.0", "end-1c")
        filtered_content = content.translate(
            str.maketrans('', '', ''.join(
                set(content) - set(allowed_chars)
            ))
        )
        self.input_field_entry.delete("1.0", "end")
        self.input_field_entry.insert("1.0", filtered_content)

        self.input_field_entry.bind(
            "<KeyPress>",
            lambda event: entry_bindings.input_filter(
                event=event,
                allowed_chars=allowed_chars
            )
        )


    def update_input_placeholder(self, text: str):
        self.input_field_entry_clear_hint(None)
        self.input_field_entry_placeholder = text
        entry_bindings.add_hint(
            self.input_field_entry,
            hint_text=self.input_field_entry_placeholder
        )


    def build(self):
        self.input_field_title.grid(
            row=0, column=0, sticky='w'
        )
        self.input_field_entry.grid(
            row=1, column=0, sticky='w'
        )
        entry_bindings.add_hint(
            parent=self.input_field_entry,
            hint_text=self.input_field_entry_placeholder
        )


if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root)
    gui = InputGUI(frame)
    frame.pack()
    gui.pack()
    root.mainloop()
