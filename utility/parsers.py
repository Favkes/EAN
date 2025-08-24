from mpmath import iv, mp


iv.prec = 64
mp.prec = 64
MAKE_FLOATY = False     # Formats all numbers with trailing zeros and adds e+0 if there's no exponent.


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


def always_look_like_float(strnum: str) -> str:
    if 'e' not in strnum:
        return f'{strnum:018s}' + 'e+0'
    return strnum


def prettify(data: iv.mpf | mp.mpf) -> str:
    if isinstance(data, mp.mpf):
        output = str(data)

        if MAKE_FLOATY:
            output = always_look_like_float(output)

        return output

    elif isinstance(data, iv.mpf):
        output = str(data)

        if MAKE_FLOATY:
            outA, outB = output[1:-1].split(', ')
            outA = always_look_like_float(outA)
            outB = always_look_like_float(outB)
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
