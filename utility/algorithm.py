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
    y_ = y.copy()
    z = z[0]

    for i in range(1, len(x)):
        for j in range(len(x) - i):
            dx_ij = z - x[i + j]
            dx_j = x[j] - z
            dx_j_ij = x[j] - x[i + j]

            y_[j] = (dx_ij * y_[j] + dx_j * y_[j + 1]) / dx_j_ij
    return y_[0]


def lagrange_coefficients(x, y) -> list[mp.mpf | iv.mpf]:
    dtype = type(x[0])
    out = [dtype(0)] * len(x)

    for i in range(len(x)):
        coeffs = [dtype(1)]
        denominator = dtype(1)

        for j in range(len(x)):
            if i == j: continue

            coeffs_tmp = [dtype(0)] * (len(coeffs) + 1)

            for k in range(len(coeffs)):
                coeffs_tmp[k]     -= coeffs[k] * x[j]
                coeffs_tmp[k + 1] += coeffs[k]

            coeffs = coeffs_tmp
            denominator *= x[i] - x[j]

        scale = y[i] / denominator
        for j in range(len(coeffs)):
            out[j] += coeffs[j] * scale

    return out
