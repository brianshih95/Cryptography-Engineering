import numpy as np
from numpy.polynomial import polynomial as poly
import pickle


def polymul(x, y, modulus, poly_mod):
    return np.int64(np.round(poly.polydiv(poly.polymul(x, y) % modulus, poly_mod)[1] % modulus))


def polyadd(x, y, modulus, poly_mod):
    return np.int64(np.round(poly.polydiv(poly.polyadd(x, y) % modulus, poly_mod)[1] % modulus))


def keygen(size, modulus, poly_mod):
    s = np.random.randint(0, 2, size, dtype=np.int64)
    a = np.random.randint(0, modulus, size, dtype=np.int64)
    e = np.int64(np.random.normal(0, 2, size=size))
    b = polyadd(polymul(-a, s, modulus, poly_mod), -e, modulus, poly_mod)
    return (b, a), s

if __name__ == "__main__":
    n = 2**4  # polynomial modulus degree
    q = 2**15  # ciphertext modulus
    poly_mod = np.array([1] + [0] * (n - 1) + [1])

    pk, sk = keygen(n, q, poly_mod)
    
    with open('server/public_key.pkl', 'wb') as f:
        pickle.dump(pk, f)
    with open('client/secret_key.pkl', 'wb') as f:
        pickle.dump(sk, f)
