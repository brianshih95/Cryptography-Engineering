def lfsr(key, polynomial, n):
    state = key
    keystream = []
    poly_len = len(polynomial)
    for _ in range(n):
        feedback = sum(int(state[j]) * int(polynomial[j % poly_len]) 
                       for j in range(len(state)))
        output_bit = state[-1]
        state = state[1:] + str(feedback % 2)
        keystream.append(output_bit)
    return ''.join(keystream)

def solve(message, key, polynomial):
    encrypted_message = ''
    keystream = lfsr(key, polynomial, len(message))
    for i in range(len(message)):
        encrypted_char = chr(ord(message[i]) ^ int(keystream[i]))
        encrypted_message += encrypted_char
    return encrypted_message

plaintext = """
ATNYCUWEARESTRIVINGTOBEAGREATUNIVERSITYTHATTRAN
SCENDSDISCIPLINARYDIVIDESTOSOLVETHEINCREASINGLYCO
MPLEXPROBLEMSTHATTHEWORLDFACESWEWILLCONTINUET
OBEGUIDEDBYTHEIDEATHATWECANACHIEVESOMETHINGMU
CHGREATERTOGETHERTHANWECANINDIVIDUALLYAFTERALLT
HATWASTHEIDEATHATLEDTOTHECREATIONOFOURUNIVERSI
TYINTHEFIRSTPLACE
"""

polynomial = "100011101"
initial_key = "00000001"

encrypted = solve(plaintext, initial_key, polynomial)
print("Encrypted message:", encrypted)

decrypted = solve(encrypted, initial_key, polynomial)
print("Decrypted message:", decrypted)
