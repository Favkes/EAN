"""
Configuration maps for input parsing and placeholders.

This module holds constants used to configure `gui.core.App`'s
entry fields' parsers, placeholders and filter masks for all three
arithmetic modes.

    - ``parser_modes_map``:
        Maps mode names to parsing functions
    - ``input_placeholder_text_map``:
        Placeholder text for input fields
    - ``input_allowed_chars_map``:
        Characters allowed inside input fields
    - ``input_new_point_placeholder_text_map``:
        Placeholder text for new point's input field
"""


from utility import parsers


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
    'real':         '-0.123,456;789 \n',
    'interval':     '-0.123,456;789[] \n',
    'singleton':    '-0.123,456;789 \n'
}
input_new_point_placeholder_text_map: dict = {
    'real':         '3.14159265359',
    'interval':     '[0;3.14159265359]',
    'singleton':    '3.14159265359'
}
