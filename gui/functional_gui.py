import tkinter as tk


def add_hint(parent: tk.Text,
             hint_text: str = "hint"):
    if not parent.get("1.0", "end-1c").strip():
        parent.insert("1.0", hint_text)
        parent.config(fg="grey")


def clear_hint(parent: tk.Text,
               hint_text: str = "hint",
               event=None):
    # print(
    #     '-clear hint',
    #     '\n>'+parent.get("1.0", "end-1c"),
    #     '\n>'+hint_text)
    if parent.get("1.0", "end-1c") == hint_text:
        parent.delete("1.0", "end")
        parent.config(fg="black")


def focus_out(parent: tk.Text,
              hint_text: str = "hint",
              event = None):
    if not parent.get("1.0", "end-1c").strip():
        add_hint(parent, hint_text=hint_text)


def input_filter(event,
                 allowed_chars: str = '0123456789.[;],\n'):
    char = event.char
    if event.keysym == 'BackSpace':
        return None
    if event.keysym in ('Return', 'KP_Enter'):
        return None
    if char and char not in allowed_chars:
        return 'break'
    return None


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
        self.input_field_entry_placeholder = ''
        self.input_field_entry_allowed_chars = '0.123,456;789\n'
        self.input_field_entry.bind(
            "<FocusIn>",
            self.input_field_entry_clearhint
        )
        self.input_field_entry.bind(
            "<FocusOut>",
            lambda event: focus_out(
                self.input_field_entry,
                hint_text=self.input_field_entry_placeholder,
                event=event
            )
        )
        self.update_input_filter()

    def input_field_entry_clearhint(self, event):
        return clear_hint(
            self.input_field_entry,
            hint_text=self.input_field_entry_placeholder,
            event=event
        )


    def update_input_filter(self, allowed_chars: str = None):
        if allowed_chars is None:
            allowed_chars = self.input_field_entry_allowed_chars
        else:
            self.input_field_entry_allowed_chars = allowed_chars
        # print('--update input filter to:', allowed_chars)

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
            lambda event: input_filter(
                event=event,
                allowed_chars=allowed_chars
            )
        )


    def update_input_placeholder(self, text: str):
        # print('--update input placeholder:\n', text)
        self.input_field_entry_clearhint(None)
        self.input_field_entry_placeholder = text
        add_hint(
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
        add_hint(
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
