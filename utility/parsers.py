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
