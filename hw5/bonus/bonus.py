import random

n_bytes = 1024 * 1024
random_bytes = bytes(random.randint(0, 255) for _ in range(n_bytes))

with open("bonus/bonus.bin", "wb") as f:
    f.write(random_bytes)

print("Random numbers generated and saved to bonus/bonus.bin")
