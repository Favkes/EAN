"""
Core application module for the GUI-based multiple-arithmetic interpolation project for EAN on CS-Sem2.

This module defines the main App class that handles the GUI structure and properties, user input,
arithmetic modes, and computation using interpolation algorithms. It also holds a utility function `make_focusable()`.

Classes:
    App: Main project structure and event manager for inputs, computation and output.

Functions:
    make_focusable(widget): Makes any Tkinter widget focusable by clicking on it.
"""


import tkinter as tk
from gui.functional_gui import InputGUI
from utility import algorithm
from gui.arithmeticmodes import *


def make_focusable(widget: tk.Widget) -> None:
    """
    Make any tkinter widget focusable.

    Makes any Tkinter widget focusable by clicking on any area that shows it as the topmost layer.
    Used for allowing defocusing of entry widgets by clicking outside of them.

    :param widget: Any tkinter widget
    :type widget: tk.Widget
    :return: None
    """

    widget.bind(
        '<Button-1>',
        lambda event: event.widget.master.focus_set()
    )


def allow_copying_contents(widget: tk.Widget) -> None:
    """
        Make any tkinter widget allow copying it's contents to the clipboard
        (if it has any).

        Makes any Tkinter widget support the Ctrl+C keybind widely used as
        "Copy to clipboard".

        :param widget: Any tkinter widget
        :type widget: tk.Widget
        :return: None
    """
    def copying_func(event=None):
        """
        Copy contents of the widget passed into allow_copying_contents().

        Copies (if possible) the contents of the specified widget into
        user's system clipboard.
        :param event: tk.Event
        :return: None
        """
        try:
            event.widget.master.event_generate("<<Copy>>")
        except:
            pass
    widget.bind("<Control-c>", copying_func)


def allow_pasting_in(widget: InputGUI) -> None:
    """
        Make gui.functional_gui.InputGUI objects allow pasting in content to inside it from
        the clipboard.

        Makes gui.functional_gui.InputGUI objects support the Ctrl+V keybind widely used as
        "Paste from clipboard".

        :param widget: Any tkinter widget
        :type widget: tk.Widget
        :param allowed_chars: A string of characters allowed in the widget
        :type allowed_chars: str
        :return: None
    """
    def pasting_func(event = None):
        """
            Paste contents of the clipboard to inside the widget passed into
            allow_pasting_in().

            Pastes in (if possible) the contents of user's system clipboard,
            and filters the data with the allowed_chars mask, if specified.
        :param event: tk.Event
        :return: None
        """
        try:
            clipboard_content = widget.clipboard_get()
            widget.input_field_entry.insert(tk.INSERT, clipboard_content)
            widget.update_input_filter()
        except tk.TclError:
            pass
        return "break"
    widget.input_field_entry.bind("<Control-v>", pasting_func)


class App:
    """
    The main class managing all components of the project, used as the main project structure.

    This class manages all pieces of the project and connects them into a working structure.
    It initializes the UI components, structures them correctly within the root window,
    manages writing outputs and handling user inputs such as button clicks and entry field interactions.
    """

    def __init__(self, root_window: tk.Tk):
        """
        Initialize a core.App instance.
        All of the app's tkinter components are initialized in here as well.

        :param root_window: Reference to the root window that core.App is supposed to be contained in.
        :type root_window: tk.Tk
        """

        self.root = root_window
        self.root.columnconfigure(0, weight=1)
        # self.root.rowconfigure(0, weight=0)
        self.mainframe = tk.Frame(self.root)
        self.mainframe.rowconfigure(1, weight=1)

        self.title_label = tk.Label(
            self.root,
            text='Lagrange\'s Interpolation and Neville\'s Algorithm',
            font=("Courier", 15)
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
            text='Singleton Interval Arithmetic',
            variable=self.current_mode,
            value='singleton',
            command=self.update_mode
        )

        self.input_frame = tk.Frame(self.mainframe)
        input_gui_x_y_width = 35
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
                                    title='Input new point\'s x:',
                                    dims=(input_gui_x_y_width * 2 + 5, 2))

        self.calculate_button_spacer = tk.Frame(self.mode_switch_frame, height=45)
        self.calculate_button = tk.Button(
            self.mode_switch_frame,
            text='Calculate',
            command=self.calculate_button_func
        )

        self.output_box = tk.Text(self.mainframe,
                                  width=input_gui_x_y_width * 2 + 28,
                                  height=10,
                                  state='disabled')

        # self.parser = lambda s: None
        self.update_mode()


    def update_mode(self):
        """
        Update the arithmetic mode for the program's computations.

        This method updates the parser and modifies the input placeholders,
        as well as allowed character masks for all relevant input fields (X, Y, Z)
        according to the currently selected mode.

        :raises Exception: If the current mode key is not valid.
        :return: None
        """

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
            input_new_point_placeholder_text_map[self.current_mode.get()]
        )
        self.input_gui_z.update_input_filter(
            input_allowed_chars_map[self.current_mode.get()]
        )


    def write_output(self, output: str):
        """
        Overwrite all contents of the output text widget with the given string.

        This method clears any existing text in `self.output_box` and inserts
        the new content. The widget is temporarily set to editable and then
        returned to the disabled state to prevent user interaction.

        :param output: The string to display in the output text widget
        :type output: str
        :return: None
        """

        self.output_box.config(state='normal')
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", output)
        self.output_box.config(state='disabled')


    def calculate_button_func(self) -> None:
        """
        Process input data from entry fields, perform interpolation algorithms, and display results.

        This method:
            1. Retrieves values from X, Y and Z entry fields.
            2. Validates that all fields are filled and correctly formatted.
            3. Checks that X and Y lists have the same length and that X contains no duplicate values.
            4. Performs Lagrange and Neville interpolations and calculates Lagrange polynomial coefficients.
            5. Outputs the results using `self.write_output()`.

        :return: None
        :raises Exception: If the input data cannot be parsed correctly.
        :side effects: Updates the contents of the output text widget (`self.output_box`).
        """

        data_x = self.input_gui_x.input_field_entry.get("1.0", "end-1c")
        data_y = self.input_gui_y.input_field_entry.get("1.0", "end-1c")
        data_z = self.input_gui_z.input_field_entry.get("1.0", "end-1c")

        # [Error] Empty field
        if '' in (data_x, data_y, data_z):
            output = 'Not all fields have been filled.'
            self.write_output(output)
            return

        # [Error] Incorrect format
        data_x = parsers.safe_parse(
            parser_func=self.parser,
            data_str=data_x,
            error_command=self.write_output,
            error_message='Incorrect data format in field \'X values\':\n{}'
        )

        # [Error] Incorrect format
        data_y = parsers.safe_parse(
            parser_func=self.parser,
            data_str=data_y,
            error_command=self.write_output,
            error_message='Incorrect data format in field \'Y values\':\n{}'
        )

        # [Error] Incorrect format
        data_z = parsers.safe_parse(
            parser_func=self.parser,
            data_str=data_z,
            error_command=self.write_output,
            error_message='Incorrect data format in field \'New Point x\':\n{}'
        )

        # [Error] Incorrect format (Message already displayed in parsers.safe_parse())
        if None in (data_x, data_y, data_z):
            return

        # [Error] Dataset sizes mismatch
        if len(data_x) != len(data_y):
            self.write_output('The number of X values does not match that of the Y values.\n'
                              f'x.size() = {len(data_x)}, y.size() = {len(data_y)}')
            return

        # size assertion (is sure to be true btw but it's there for convention's sake)
        assert len(data_x) > 0
        assert len(data_y) > 0
        assert len(data_z) > 0

        # Duplicate check
        # [Error] X dataset contains duplicates
        if len(set(data_x)) < len(data_x):
            self.write_output('The X values contain duplicates, which is forbidden.')
            return

        # print('x', data_x)
        # print('y', data_y)
        # print('z', data_z)

        output1 = algorithm.lagrange(
            data_x,
            data_y,
            data_z
        )
        output2 = algorithm.neville(
            data_x,
            data_y,
            data_z
        )
        output3 = algorithm.lagrange_coefficients(
            data_x,
            data_y
        )
        # sgn, man, exp, bic = output._mpf_
        # print(sgn, bin(man)[2:], exp, bic)

        self.write_output(
            f'Lagrange Interpolation: \n{parsers.prettify(output1)}\n'
            f'Neville Interpolation: \n{parsers.prettify(output2)}\n'
            f'Lagrange Polynomial Coefficients: \n{parsers.prettify(output3)}'
        )


    def build(self):
        """
        Structure the contents of the app using tkinter's grid geometry manager,
        set correct properties for specific widgets.

        :return: None
        """

        make_focusable(self.title_label)
        make_focusable(self.mainframe)
        make_focusable(self.mode_switch_frame)
        make_focusable(self.mode_switch_A)
        make_focusable(self.mode_switch_B)
        make_focusable(self.mode_switch_C)
        make_focusable(self.input_frame)
        allow_copying_contents(self.input_gui_x.input_field_entry)
        allow_copying_contents(self.input_gui_y.input_field_entry)
        allow_copying_contents(self.input_gui_z.input_field_entry)
        allow_pasting_in(self.input_gui_x)
        allow_pasting_in(self.input_gui_y)
        allow_pasting_in(self.input_gui_z)

        self.title_label.grid(
            row=0, column=0, sticky='ew'
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
            input_new_point_placeholder_text_map[self.current_mode.get()]
        )
        self.input_gui_z.build()

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
        """
        Place all the app's elements in the root window and run the window.

        :return: None
        """

        self.title_label.pack(fill='both', expand=True)
        self.mainframe.pack(fill='both', expand=True)
        self.root.mainloop()


    def debug_mode(self):
        """
        Enable debug mode by coloring the backgrounds of key widgets
        to clearly show the app layout.

        This method must be called explicitly to activate the debug mode.
        It changes the background colors of main UI elements for debugging purposes.

        :return: None
        :side effects: Updates the background colors of multiple (but not all) widgets.
        """

        self.mainframe.config(bg='pink')
        self.title_label.config(bg='red')
        self.input_frame.config(bg='cyan')
        self.input_gui_x.config(bg='blue')
        self.input_gui_y.config(bg='yellow')
        self.mode_switch_frame.config(bg='green')
        self.output_box.config(bg='magenta')
