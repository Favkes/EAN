import tkinter as tk
from gui.functional_gui import InputGUI
from utility import parsers


class App:
    def __init__(self, root_window: tk.Tk):
        self.root = root_window
        self.mainframe = tk.Frame(self.root)

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

        self.functional_gui = InputGUI(self.mainframe)
        self.parser = lambda s: None
        # self.interval_gui = IntervalGUI(self.mainframe)
        # self.singleton_gui = SingletonGUI(self.mainframe)

        self.parser_modes_map = {
            'real': parsers.parse_real,
            'interval': parsers.parse_interval,
            'singleton': parsers.parse_singleton
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


    def update_mode(self):
        if self.current_mode.get() not in self.parser_modes_map.keys():
            raise Exception(f'Incorrect mode key request: {self.current_mode.get()}')

        # for mode in self.modes_map.values():
        #     mode.grid_remove()

        self.parser = self.parser_modes_map[self.current_mode.get()]


    def display(self):
        self.title_label.pack(anchor='n')
        self.mainframe.pack(side='left')
        self.root.mainloop()
