#!/usr/bin/python3
import random
import argparse

### DATA START
letter2code = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--.."
}

letters = letter2code.keys()
codes = letter2code.values()
sorted_letters = sorted(letters)
assert len(letters) == len(set(letters))
assert len(letters) == 26
assert sorted_letters[0] == "A"
assert sorted_letters[-1] == "Z"
assert all(map(lambda code: all(map(lambda symbol: symbol in ".-", code)), codes))
assert len(set(codes)) == len(codes)
assert len(codes) == 26
### DATA END

## CLI START
def positive_int(n):
    int_n = int(n)
    if int_n > 0:
        return int_n
    else:
        raise ValueError("n must be positive")

LETTER2CODE = 1
CODE2LETTER = 2
parser = argparse.ArgumentParser(description="Morse code learning app")
parser.add_argument(
    "--mode", "-m",
    choices=[LETTER2CODE, CODE2LETTER],
    default=LETTER2CODE,
    type=int,
    help="1: letter->code\n2: code->letter"
)
parser.add_argument(
    "-n",
    type=positive_int,
    default=1,
    help="The length of sequences to guess"
)
args = parser.parse_args()

if args.mode == LETTER2CODE:
    sorted_keys = sorted_letters
    selected_dict = letter2code
else:
    sorted_keys = sorted(codes)
    reversed_dict = {}
    for letter in letter2code:
        reversed_dict[letter2code[letter]] = letter
    selected_dict = reversed_dict
### CLI END

while True:
    random_keys = []
    correct = []
    while len(random_keys) < args.n:
        random_key = random.choice(sorted_keys)
        if random_key in random_keys:
            continue
        random_keys.append(random_key)
        correct.append(selected_dict[random_key].lower())

    while True:
        try:
            received_raw = input(f"{' '.join(random_keys)} ")
        except:
            print()
            exit()

        received_lower = received_raw.lower()
        received = [part.strip() for part in received_lower.strip().split()]
        if not received:
            continue
        if received == correct or list(received_lower.strip()) == correct:
            break

        print("Wrong!")

    print("Correct!\n")

