# Diffie-Hellman key exchange

import random


p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1
p *= 0x29024E088A67CC74020BBEA63B139B22514A08798E3404DD
p *= 0xEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245
p *= 0xE485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED
p *= 0xEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE65381
p *= 0xFFFFFFFFFFFFFFFF

g = 2


# User A generates private key a and calculate public key A
a = random.randint(1, p-1)
A = pow(g, a, p)

# User B generates private key b and calculate public key B
b = random.randint(1, p-1)
B = pow(g, b, p)

# User A calculate shared key sA
sA = pow(B, a, p)

# User B calculate shared key sB
sB = pow(A, b, p)

print(f"User A's private key: {a}")
print(f"User A's public key: {A}")
print(f"User B's private key: {b}")
print(f"User B's public key: {B}")
print(f"User A's calculated shared key': {sA}")
print(f"User B's calculated shared key': {sB}")

# Confirm that the shared keys are the same
assert sA == sB, "Shared keys are different!"
print("Shared keys are the same, key exchanged successfully!")
