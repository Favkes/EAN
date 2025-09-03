"""
Core algorithms module containing all numeric functions performed by the application.

This module contains the three algorithms performed by the application:
    - `lagrange()`:
        Lagrange's Polynomial Interpolation algorithm.
    - `neville()`:
        Neville's Interpolation algorithm.
    - `lagrange_coefficients()`:
        Computes Lagrange Interpolation Polynomial's coefficients.

All three functions are constructed to work explicitly on mpmath floating point numbers and floating point intervals.
"""


from mpmath import iv, mp


iv.prec = 64
mp.prec = 64


def lagrange(arr_x, arr_y, arr_z) -> mp.mpf | iv.mpf:
    dtype = type(arr_x[0])
    result = dtype(0)
    for i in range(len(arr_x)):
        term = arr_y[i]
        for j in range(len(arr_x)):
            if i == j: continue
            numerator = arr_z[0] - arr_x[j]
            denominator = arr_x[i] - arr_x[j]
            fraction = numerator / denominator

            term = term * fraction
        result = result + term
    return result


def neville(arr_x, arr_y, arr_z) -> mp.mpf | iv.mpf:
    y_ = arr_y.copy()
    arr_z = arr_z[0]

    for i in range(1, len(arr_x)):
        for j in range(len(arr_x) - i):
            dx_ij = arr_z - arr_x[i + j]
            dx_j = arr_x[j] - arr_z
            dx_j_ij = arr_x[j] - arr_x[i + j]

            y_[j] = (dx_ij * y_[j] + dx_j * y_[j + 1]) / dx_j_ij
    return y_[0]


def lagrange_coefficients(arr_x, arr_y) -> list:
    dtype = type(arr_x[0])
    out = [dtype(0)] * len(arr_x)

    for i in range(len(arr_x)):
        coeffs = [dtype(1)]
        denominator = dtype(1)

        for j in range(len(arr_x)):
            if i == j: continue

            coeffs_tmp = [dtype(0)] * (len(coeffs) + 1)

            for k in range(len(coeffs)):
                coeffs_tmp[k]     -= coeffs[k] * arr_x[j]
                coeffs_tmp[k + 1] += coeffs[k]

            coeffs = coeffs_tmp
            denominator *= arr_x[i] - arr_x[j]

        scale = arr_y[i] / denominator
        for j in range(len(coeffs)):
            out[j] += coeffs[j] * scale

    return out
