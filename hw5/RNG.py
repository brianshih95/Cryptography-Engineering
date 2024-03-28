import secrets

n_bytes = 1024 * 1024
random_bytes = secrets.token_bytes(n_bytes)

with open("random.bin", "wb") as f:
    f.write(random_bytes)

print("Random numbers generated and saved to random.bin")
