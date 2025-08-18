import tkinter as tk
from gui.real_numbers import RealGUI
from gui.interval_numbers import IntervalGUI
from gui.singleton_numbers import SingletonGUI


class App:
    def __init__(self, root_window: tk.Tk):
        self.root = root_window
        self.mainframe = tk.Frame(self.root)

        self.title_label = tk.Label(
            self.mainframe,
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

        self.real_gui = RealGUI(self.mainframe)
        self.interval_gui = IntervalGUI(self.mainframe)
        self.singleton_gui = SingletonGUI(self.mainframe)

        self.modes_map = {
            'real': self.real_gui,
            'interval': self.interval_gui,
            'singleton': self.singleton_gui
        }

        self.real_gui.grid(
            row=1, column=1
        ); self.real_gui.grid_remove()

        self.interval_gui.grid(
            row=1, column=1
        ); self.interval_gui.grid_remove()

        self.singleton_gui.grid(
            row=1, column=1
        ); self.singleton_gui.grid_remove()


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
        self.real_gui.grid()


    def update_mode(self):
        if self.current_mode.get() not in self.modes_map.keys():
            raise Exception(f'Incorrect mode key request: {self.current_mode.get()}')

        for mode in self.modes_map.values():
            mode.grid_remove()

        self.modes_map[self.current_mode.get()].grid()


    def display(self):
        self.mainframe.pack(anchor='w')
        self.root.mainloop()
