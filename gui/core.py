import tkinter as tk
from gui.functional_gui import InputGUI
from utility import parsers


def make_focusable(widget: tk.Widget):
    widget.bind(
        '<Button-1>',
        lambda event: event.widget.master.focus_set()
    )


def calculate_button_func(input_x: InputGUI, input_y: InputGUI, input_z: InputGUI):
    data_x = input_x.input_field_entry.get("1.0", "end-1c")
    data_y = input_y.input_field_entry.get("1.0", "end-1c")
    data_z = input_z.input_field_entry.get("1.0", "end-1c")

    print(data_x)
    print(data_y)
    print(data_z)


parser_modes_map: dict = {
    'real':         parsers.parse_real,
    'interval':     parsers.parse_interval,
    'singleton':    parsers.parse_singleton
}
input_placeholder_text_map: dict = {
    'real':         '0,\n1,2, 3',
    'interval':     '[0;1],\n[2.34; 5], [6.7, 8]',
    'singleton':    '0,\n1,2, 3'
}
input_allowed_chars_map: dict = {
    'real':         '0.123,456;789 \n',
    'interval':     '0.123,456;789[] \n',
    'singleton':    '0.123,456;789 \n'
}


class App:
    def __init__(self, root_window: tk.Tk):
        self.root = root_window
        self.mainframe = tk.Frame(self.root)
        self.mainframe.rowconfigure(1, weight=1)

        self.parser = lambda s: None

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

        self.input_frame = tk.Frame(self.mainframe)
        self.input_gui_x = InputGUI(self, self.input_frame, title='Input X values:')
        self.input_gui_y = InputGUI(self, self.input_frame, title='Input Y values:')
        self.input_gui_z = InputGUI(self,
                                    self.input_frame,
                                    title='Input the point\'s x:',
                                    dims=(45, 2))

        self.calculate_button = tk.Button(
            self.input_frame,
            text='Calculate',
            command=lambda : calculate_button_func(self.input_gui_x, self.input_gui_y, self.input_gui_z)
        )

        self.output_box = tk.Text(self.mainframe, width=80, height=10, state='disabled')


    def update_mode(self):
        if self.current_mode.get() not in parser_modes_map.keys():
            raise Exception(f'Incorrect mode key request: {self.current_mode.get()}')

        self.parser = parser_modes_map[self.current_mode.get()]

        # Input X
        self.input_gui_x.update_input_placeholder(
            input_placeholder_text_map[self.current_mode.get()]
        )
        self.input_gui_x.update_input_filter(
            input_allowed_chars_map[self.current_mode.get()]
        )

        # Input Y
        self.input_gui_y.update_input_placeholder(
            input_placeholder_text_map[self.current_mode.get()]
        )
        self.input_gui_y.update_input_filter(
            input_allowed_chars_map[self.current_mode.get()]
        )

        # Input Z (new point's X)
        self.input_gui_z.update_input_placeholder(
            input_placeholder_text_map[self.current_mode.get()]
        )
        self.input_gui_z.update_input_filter(
            input_allowed_chars_map[self.current_mode.get()]
        )


    def build(self):
        make_focusable(self.mainframe)
        make_focusable(self.mode_switch_frame)
        make_focusable(self.mode_switch_A)
        make_focusable(self.mode_switch_B)
        make_focusable(self.mode_switch_C)
        make_focusable(self.input_frame)

        self.title_label.grid(
            row=0, column=0, sticky='w'
        )

        self.mode_switch_frame.grid(
            row=0, column=0, sticky='w'
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

        self.input_frame.grid(
            row=0, column=1
        )
        self.input_gui_x.grid(
            row=0, column=0
        )
        self.input_gui_x.update_input_placeholder(
            input_placeholder_text_map[self.current_mode.get()]
        )
        self.input_gui_x.build()

        self.input_gui_y.grid(
            row=0, column=1
        )
        self.input_gui_y.update_input_placeholder(
            input_placeholder_text_map[self.current_mode.get()]
        )
        self.input_gui_y.build()

        self.input_gui_z.grid(
            row=1, column=0, columnspan=2, pady=5
        )
        self.input_gui_z.update_input_placeholder(
            input_placeholder_text_map[self.current_mode.get()]
        )
        self.input_gui_z.build()

        self.calculate_button.grid(
            row=2, column=0, columnspan=2, pady=10
        )

        self.output_box.grid(
            row=1, column=0, columnspan=2
        )


    def display(self):
        self.title_label.pack(anchor='n')
        self.mainframe.pack(fill='both', expand=True)
        self.root.mainloop()


    def debug_mode(self):
        self.mainframe.config(bg='pink')
        self.title_label.config(bg='red')
        self.input_frame.config(bg='cyan')
        self.input_gui_x.config(bg='blue')
        self.input_gui_y.config(bg='yellow')
        self.mode_switch_frame.config(bg='green')
        self.output_box.config(bg='magenta')
