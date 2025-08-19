from mpmath import iv


def parse_real(s: str):
    s = s.replace(' ', '')
    args = s.split(',')
    return [int(x) for x in args]


def parse_singleton(s: str):
    return [iv.mpf([x, x]) for x in parse_real(s)]


def parse_interval(s: str):
    s = s.replace(' ', '')
    s = s.replace('[', '').replace(']', '').replace(';', ',')
    args = s.split(',')
    args = [int(x) for x in args]
    return [
        iv.mpf([
            min(args[i], args[i+1]),
            max(args[i], args[i+1])
        ])
        for i in range(0, len(args), 2)
    ]


if __name__ == "__main__":
    print(parse_interval(
        "[1;2], [4;5],[7,9] , [11, 10]"
    ))
    print(
        parse_singleton(
            "1, 2, 5, 6"
        )
    )
