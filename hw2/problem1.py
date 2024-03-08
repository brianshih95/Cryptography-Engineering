import hashlib
import time

def find_salt(passwords, tries):
    for password in passwords:
        tries += 1
        hashed = hashlib.sha1(password.encode()).hexdigest()
        if hashed == 'dfc3e4f0b9b5fb047e9be9fb89016f290d2abb06':
            salt = password
            return salt, tries
    return None, 0

def solve(name, hash, passwords):
    start_time = time.time()
    tries = 0
    
    if name == 'Leet hacker hash':
        salt, tries = find_salt(passwords, tries)
    
    for password in passwords:
        tries += 1
        
        if name == 'Leet hacker hash':
            final_password = salt + password
        else:
            final_password = password
        
        hashed = hashlib.sha1(final_password.encode()).hexdigest()
        if hashed == hash:
            end_time = time.time()
            time_taken = end_time - start_time
            return password, tries, time_taken
    
    return None, tries, None

file_path = 'password.txt'
with open(file_path, 'r') as file:
    passwords =  [line.strip() for line in file]

SHA1_hashes = {
    'Easy hash': 'ef0ebbb77298e1fbd81f756a4efc35b977c93dae',
    'Medium hash': '0bc2f4f2e1f8944866c2e952a5b59acabd1cebf2',
    'Leet hacker hash': '9d6b628c1f81b4795c0266c0f12123c1e09a7ad3',
}

for name, hash in SHA1_hashes.items():
    password, tries, time_taken = solve(name, hash, passwords)
    print(f"Hash: {hash}")
    print(f"Password: {password}")
    print(f"Took {tries} attempts to crack input hash. Time Taken: {time_taken:.6f} seconds\n")
