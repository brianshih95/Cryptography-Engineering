# RSA

import random
from sympy import isprime, gcd, mod_inverse


def generate_prime_candidate(length):
    p = random.getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p


def generate_prime(length=1024):
    p = 0
    while not isprime(p):
        p = generate_prime_candidate(length)
    return p


def generate_keypair(keysize):
    p = generate_prime(keysize)
    q = generate_prime(keysize)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = mod_inverse(e, phi)

    return ((e, n), (d, n))


def encrypt(keypair, plaintext):
    key, n = keypair
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher


def decrypt(keypair, ciphertext):
    key, n = keypair
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)


message = "Cryptography Engineering"

# Key generation
public, private = generate_keypair(512)

print("Public key:", public)
print("Private key:", private)

# Encryption
encrypted_msg = encrypt(public, message)
print("Encrypted message:", encrypted_msg)

# Decryption
decrypted_msg = decrypt(private, encrypted_msg)
print("Plaintext:", message)
print("Decrypted message:", decrypted_msg)

assert message == decrypted_msg, "Wrong message!"
print("Plaintext and decrypted message are the same, decrypted successfully!")
