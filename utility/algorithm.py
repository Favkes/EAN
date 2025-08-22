from mpmath import iv, mp


iv.prec = 64
mp.prec = 64


def lagrange(x, y, z) -> mp.mpf | iv.mpf:
    out = []
    for x_, y_ in zip(x, y):
        out.append(x_ + y_)
    return out


def neville() -> mp.mpf | iv.mpf:
    return None
