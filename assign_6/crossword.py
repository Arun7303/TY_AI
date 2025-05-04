from itertools import product

def crossword_solver():
    words = ["HELLO", "HOUSE", "SOLAR", "SHORE", "LARGE", "LEARN", "ROSES"]
    slot1 = slot2 = slot3 = words

    for w1, w2, w3 in product(slot1, slot2, slot3):
        if w1[0] == w2[0] and w2[2] == w3[2]:
            print(f"Slot1 (across): {w1}")
            print(f"Slot2 (down):   {w2}")
            print(f"Slot3 (across): {w3}")
            return

crossword_solver()
