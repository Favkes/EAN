import tkinter as tk
from gui.functional_gui import InputGUI
from utility import parsers


def make_focusable(widget: tk.Widget):
    widget.bind(
        '<Button-1>',
        lambda event: event.widget.master.focus_set()
    )


class App:
    def __init__(self, root_window: tk.Tk):
        self.root = root_window
        self.mainframe = tk.Frame(self.root)
        self.mainframe.rowconfigure(1, weight=1)
        make_focusable(self.mainframe)

        self.title_label = tk.Label(
            self.root,
            text='Oto nowa ma wytyczna - Analiza Numeryczna!'
        )

        self.mode_switch_frame = tk.Frame(self.mainframe)
        self.current_mode = tk.StringVar(value='real')
        self.mode_switch_A = tk.Radiobutton(
            self.mode_switch_frame,
            text='Real Arithmetic',
            variable=self.current_mode,
            value='real',
            command=self.update_mode
        )
        self.mode_switch_B = tk.Radiobutton(
            self.mode_switch_frame,
            text='Interval Arithmetic',
            variable=self.current_mode,
            value='interval',
            command=self.update_mode
        )
        self.mode_switch_C = tk.Radiobutton(
            self.mode_switch_frame,
            text='Singleton Arithmetic',
            variable=self.current_mode,
            value='singleton',
            command=self.update_mode
        )
        make_focusable(self.mode_switch_frame)
        make_focusable(self.mode_switch_A)
        make_focusable(self.mode_switch_B)
        make_focusable(self.mode_switch_C)

        self.functional_gui = InputGUI(self.mainframe)
        self.parser = lambda s: None
        # self.interval_gui = IntervalGUI(self.mainframe)
        # self.singleton_gui = SingletonGUI(self.mainframe)

        self.parser_modes_map: dict = {
            'real': parsers.parse_real,
            'interval': parsers.parse_interval,
            'singleton': parsers.parse_singleton
        }

        self.input_placeholder_text_map: dict = {
            'real': '0,\n1,2, 3',
            'interval': '[0;1],\n[2.34; 5], [6.7, 8]',
            'singleton': '0,\n1,2, 3'
        }
        self.input_allowed_chars_map: dict = {
            'real': '0.123,456;789 \n',
            'interval': '0.123,456;789[] \n',
            'singleton': '0.123,456;789 \n'
        }


    def build(self):
        self.title_label.grid(
            row=0, column=0, sticky='w'
        )

        self.mode_switch_frame.grid(
            row=1, column=0, sticky='w'
        )
        self.mode_switch_A.grid(
            row=0, column=0, sticky='w'
        )
        self.mode_switch_B.grid(
            row=1, column=0, sticky='w'
        )
        self.mode_switch_C.grid(
            row=2, column=0, sticky='w'
        )

        self.functional_gui.grid(
            row=1, column=1
        )
        self.functional_gui.update_input_placeholder(
            self.input_placeholder_text_map[self.current_mode.get()]
        )

        self.functional_gui.build()


    def update_mode(self):
        if self.current_mode.get() not in self.parser_modes_map.keys():
            raise Exception(f'Incorrect mode key request: {self.current_mode.get()}')

        self.parser = self.parser_modes_map[self.current_mode.get()]

        self.functional_gui.update_input_placeholder(
            self.input_placeholder_text_map[self.current_mode.get()]
        )
        self.functional_gui.update_input_filter(
            self.input_allowed_chars_map[self.current_mode.get()]
        )
        # self.functional_gui.update_input_filter()


    def display(self):
        self.title_label.pack(anchor='n')
        self.mainframe.pack(fill='both', expand=True)
        self.root.mainloop()


    def debug_mode(self):
        self.mainframe.config(bg='pink')
        self.title_label.config(bg='red')
        self.functional_gui.config(bg='blue')
        self.mode_switch_frame.config(bg='green')
