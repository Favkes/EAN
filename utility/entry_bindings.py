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
