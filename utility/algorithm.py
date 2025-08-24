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
    return result


def neville(x, y, z) -> mp.mpf | iv.mpf:
    y_data = y.copy()

    for i in range(1, len(x)):
        for j in range(len(x) - i):
            dx_ij = z - x[i + j]
            dx_j = x[j] - z
            dx_j_ij = x[j] - x[i + j]
            print(i, j)

            y[j] = (dx_ij * y[j] + dx_j * y[j + 1]) / dx_j_ij
    return y[0]
