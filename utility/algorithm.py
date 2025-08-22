from mpmath import iv, mp


iv.prec = 64
mp.prec = 64


def lagrange(x, y, z) -> mp.mpf | iv.mpf:
    dtype = type(x[0])
    result = dtype(0)
    for i in range(len(x)):
        term = y[i]
        for j in range(len(x)):
            if i == j: continue
            numerator = z[0] - x[j]
            denominator = x[i] - x[j]
            fraction = numerator / denominator

            term = term * fraction
        result = result + term
    sgn, man, exp, bic = result._mpf_
    print(sgn, bin(man)[2:], exp, bic)
    return result


def neville() -> mp.mpf | iv.mpf:
    return None
