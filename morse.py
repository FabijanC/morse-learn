#!/usr/bin/python3

"""
This is a CLI program for learning Morse code.
After starting the program, you are prompted with cues, to which you respond by typing the answer:

1. in letter-to-code mode, type the Morse code of the given letter by using dots (.) and dashes (-)
2. in code-to-letter mode, type the letter corresponding to the shown Morse code

Exit by pressing Ctrl+D.
"""

import random
import argparse
import sys

import data


## CLI CONFIG START
def positive_int(n):
    """Parse positive int"""
    int_n = int(n)
    if int_n > 0:
        return int_n
    raise ValueError("value must be positive")


LETTER_TO_CODE_SELECTOR = "letter-to-code"
CODE_TO_LETTER_SELECTOR = "code-to-letter"

parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--mode",
    "-m",
    type=str,
    choices=[LETTER_TO_CODE_SELECTOR, CODE_TO_LETTER_SELECTOR],
    default=LETTER_TO_CODE_SELECTOR,
    help="Selector of what is prompted",
)
parser.add_argument(
    "-n",
    type=positive_int,
    default=1,
    help="The length of sequences to guess",
)
args = parser.parse_args()

print("Selected mode:", args.mode)
if args.mode == LETTER_TO_CODE_SELECTOR:
    keys = list(data.letter2code.keys())
    selected_dict = data.letter2code
    print("Respond with dots and dashes.")
    if args.n > 1:
        print("Separate the codes with spaces.")
else:
    keys = sorted(data.codes)
    selected_dict = {code: letter for letter, code in data.letter2code.items()}

print("Press Ctrl+D or Ctrl+C to exit\n")
### CLI CONFIG END

while True:
    random_keys = []
    correct = []
    while len(random_keys) < args.n:
        random_key = random.choice(keys)
        if random_key in random_keys:
            continue
        random_keys.append(random_key)
        correct.append(selected_dict[random_key].lower())

    while True:
        try:
            received_raw = input(f"{' '.join(random_keys)} ")
        except (KeyboardInterrupt, EOFError):
            # Handles Ctrl+C, Ctrl+D
            print()
            sys.exit()

        received_lower = received_raw.lower()
        received = [part.strip() for part in received_lower.strip().split()]
        if not received:
            continue
        if received == correct or list(received_lower.strip()) == correct:
            break

        print("Wrong!")

    print("Correct!\n")
