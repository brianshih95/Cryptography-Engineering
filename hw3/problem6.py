def str_to_hex(s):
    return int(s.encode().hex(), 16)

ciphertext = 0x6c73d5240a948c86981bc294814d
key = str_to_hex('attack at dawn') ^ ciphertext
ans = hex(str_to_hex('defend at noon') ^ key)
print(ans)
