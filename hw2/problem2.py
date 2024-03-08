import hashlib
import time

def solve(data, hash_function):
    start_time = time.time()
    hash_function.update(data)
    hashed = hash_function.hexdigest()
    end_time = time.time()
    time_taken = end_time - start_time
    return hashed, time_taken

hash_functions = {
    "MD5": hashlib.md5(),
    "SHA1": hashlib.sha1(),
    "SHA224": hashlib.sha224(),
    "SHA256": hashlib.sha256(),
    "SHA512": hashlib.sha512(),
    "SHA3-224": hashlib.sha3_224(),
    "SHA3-256": hashlib.sha3_256(),
    "SHA3-512": hashlib.sha3_512()
}

file_path = "video.mp4"
with open(file_path, 'rb') as f:
    data = f.read()
    for name, hash_function in hash_functions.items():
        checksum, time_taken = solve(data, hash_function)
        print(f"{name}: {time_taken:.6f} seconds\n")
