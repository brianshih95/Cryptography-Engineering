import random

def naive_shuffle(cards):
    counts = {}
    for _ in range(1000000):
        shuffled_cards = cards[:]
        for i in range(len(shuffled_cards)):
            n = random.randint(0, len(shuffled_cards) - 1)
            shuffled_cards[i], shuffled_cards[n] = shuffled_cards[n], shuffled_cards[i]
        
        counts[tuple(shuffled_cards)] = counts.get(tuple(shuffled_cards), 0) + 1
    return counts

def fisher_yates_shuffle(cards):
    counts = {}
    for _ in range(1000000):
        shuffled_cards = cards[:]
        for i in range(len(shuffled_cards) - 1, 0, -1):
            n = random.randint(0, i)
            shuffled_cards[i], shuffled_cards[n] = shuffled_cards[n], shuffled_cards[i]
        
        counts[tuple(shuffled_cards)] = counts.get(tuple(shuffled_cards), 0) + 1
    return counts

cards = [1, 2, 3, 4]

print("Naive algorithm:")
naive_counts = naive_shuffle(cards)
for combination, count in naive_counts.items():
    print(f"{list(combination)}: {count}")

print("\nFisher-Yates shuffle:")
fisher_yates_counts = fisher_yates_shuffle(cards)
for combination, count in fisher_yates_counts.items():
    print(f"{list(combination)}: {count}")
