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
