import tkinter as tk
from gui.functional_gui import InputGUI
from utility import parsers
from utility import algorithm


def make_focusable(widget: tk.Widget):
    widget.bind(
        '<Button-1>',
        lambda event: event.widget.master.focus_set()
    )


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
        input_gui_x_y_width = 25
        self.input_gui_x = InputGUI(self,
                                    self.input_frame,
                                    title='Input X values:',
                                    dims=(input_gui_x_y_width, 5))
        self.input_gui_y = InputGUI(self,
                                    self.input_frame,
                                    title='Input Y values:',
                                    dims=(input_gui_x_y_width, 5))
        self.input_gui_z = InputGUI(self,
                                    self.input_frame,
                                    title='Input the point\'s x:',
                                    dims=(input_gui_x_y_width * 2 + 5, 2))

        self.calculate_button = tk.Button(
            self.mode_switch_frame,
            text='Calculate',
            command=self.calculate_button_func
        )

        self.output_box = tk.Text(self.mainframe,
                                  width=input_gui_x_y_width * 2 + 27,
                                  height=10,
                                  state='disabled')

        # self.parser = lambda s: None
        self.update_mode()


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


    def calculate_button_func(self):
        data_x = self.input_gui_x.input_field_entry.get("1.0", "end-1c")
        data_y = self.input_gui_y.input_field_entry.get("1.0", "end-1c")
        data_z = self.input_gui_z.input_field_entry.get("1.0", "end-1c")

        data_x = self.parser(data_x)
        data_y = self.parser(data_y)
        data_z = self.parser(data_z)

        print('x', data_x)
        print('y', data_y)
        print('z', data_z)

        output = algorithm.lagrange(
            data_x,
            data_y,
            data_z
        )

        output = str(output)
        print(output)

        self.output_box.config(state='normal')
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", output)
        self.output_box.config(state='disabled')


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

        self.calculate_button_spacer = tk.Frame(self.mode_switch_frame, height=45)
        self.calculate_button_spacer.grid(
            row=3, column=0
        )
        self.calculate_button.grid(
            row=4, column=0, columnspan=1, pady=0, sticky='n'
        )

        self.output_box.grid(
            row=1, column=0, columnspan=2, padx=4, sticky='w'
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
