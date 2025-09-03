"""
Data extraction module containing all the parsing functions used to convert user input into actual numeric data.

This module contains several parsing and formatting functions used in the gui.core module to convert
string numbers into actual ``mpmath`` numeric objects for all three arithmetic modes, as well as a means of
safely embedding these parsing functions to error-proof the application. There are also functions used
for formatting the output data right before writing it to the output widget.

Functions
---------

    - ``parse_real(s)``
        Converts numeric array string into an ``mp.mpf`` list
    - ``parse_singleton(s)``
        Converts numeric array string into a list of ``iv.mpf`` singleton intervals ``[a; a]``
    - ``parse_interval(s)``
        Converts numeric interval array string into a list of ``iv.mpf`` intervals ``[a; b]``
    - ``safe_parse(parser_func, data_str, error_command, error_message)``
        Embeds execution of the parser_func function in an exception block, allowing for configurable error
        feedback display directly to the output widget.
    - ``sci_str(x, prec)``
        Converts an ``mp.mpf`` number into a numeric string in the scientific format, with defined digital precision.
    - ``prettify(data)``
        Formats the output data of any of the 3 algorithms implemented in the project into human-readable text
        ready to be printed in the output widget.
"""


from mpmath import iv, mp


iv.prec = 64
mp.prec = 64


def parse_real(s: str) -> list[float]:
    s = s.replace(' ', '').replace('\n', '')
    args = s.split(',')
    return [mp.mpf(x) for x in args]


def parse_singleton(s: str) -> list:
    return [iv.mpf([x, x]) for x in parse_real(s)]


def parse_interval(s: str) -> list:
    s = s.replace(' ', '').replace('\n', '')
    s = s.replace('[', '').replace(']', '').replace(';', ',')
    args = s.split(',')
    args = [mp.mpf(x) for x in args]
    return [
        iv.mpf([
            min(args[i], args[i+1]),
            max(args[i], args[i+1])
        ])
        for i in range(0, len(args), 2)
    ]


def safe_parse(parser_func,
               data_str: str,
               error_command = lambda e: print(e),
               error_message: str = '{}'):
    try:
        return parser_func(data_str)
    except ValueError as e:
        e = str(e)
        e = e[:e.rfind("'")]
        e = e[e.rfind("'"):]
        error_command(error_message.format(e)+'\'')
        return None


def sci_str(x, prec: int = 18):
    """
    Convert mpmath.mpf to string in the form 1.234E+0001
    """
    # mantissa and exponent (in base 10)

    if x == 0:
        return "0." + '0'*prec + 'E+0000'

    exp = mp.floor(mp.log10(abs(x))) if x != 0 else 0
    mant = x / mp.power(10, exp)

    # round mantissa to desired digits
    mant_str = mp.nstr(mant, n=prec + 1, strip_zeros=False)

    # format exponent padded to 4 digits with sign
    exp_str = f"{int(exp):+05d}"

    return f"{mant_str}E{exp_str}"


def prettify(data: iv.mpf | mp.mpf | list) -> str:
    if isinstance(data, mp.mpf):
        output = sci_str(data)
        return output

    elif isinstance(data, iv.mpf):
        output = str(data)

        outA, outB = output[1:-1].split(', ')
        outA, outB = mp.mpf(outA), mp.mpf(outB)
        outA = sci_str(outA)
        outB = sci_str(outB)
        output = f'[{outA}, {outB}]'

        return output

    elif isinstance(data, list) and \
        (isinstance(data[0], mp.mpf) or
         isinstance(data[0], iv.mpf)):
        output = '[\n'
        for val in data:
            val = prettify(val)
            if val.startswith('T'):
                return 'Type error at utility.parsers.prettify():\n'+str(type(data))+' is an incorrect type.'

            output += f' {val},\n'
        output = output[:-2] + '\n]'
        return output

    else: return 'Type error at utility.parsers.prettify():\n'+str(type(data))+' is an incorrect type.'


if __name__ == "__main__":
    print(parse_interval(
        "[1;2], [4;5],[7,9] , [11, 10]"
    ))
    print(
        parse_singleton(
            "1, 2, 5, 6"
        )
    )
    print(
        parse_real(
            "2, 3, 5,7, 11"
        )
    )
