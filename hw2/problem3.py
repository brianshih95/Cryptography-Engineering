cipher = "UONCSVAIHGEPAAHIGIRLBIECSTECSWPNITETIENOIEEFDOWECXTRSRXSTTARTLODYFSOVNEOECOHENIODAARQNAELAFSGNOPTE"
vowels = 'AEIOU'

row_n = 14
text = [""] * row_n

for i in range(row_n):
    for j in range(i, len(cipher), row_n):
        text[i] += cipher[j]

difference = 0
for s in text:
    vowel_n = sum(s.count(char) for char in vowels)
    diff = abs(vowel_n - len(s) * 0.4)
    difference += diff
    print(s, vowel_n, f'{diff:.2f}')
print(f'The average difference of each row is {difference / len(text)}\n')

for i in range(row_n):
    print(text[i][4], text[i][1], text[i][5],
          text[i][6], text[i][0], text[i][3], text[i][2], sep='')
# 5267143