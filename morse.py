#!/usr/bin/env python3

"""
This is a CLI program for learning Morse code.
After starting the program, you are prompted with cues, to which you respond by typing the answer:

1. in letter-to-code mode, type the Morse code of the given letter by using dots (.) and dashes (-)
2. in code-to-letter mode, type the letter corresponding to the shown Morse code

Exit by pressing Ctrl+D.
"""

import argparse
import sys

import game_modes


## CLI CONFIG START
def positive_int(n):
    """Parse positive int"""
    int_n = int(n)
    if int_n > 0:
        return int_n
    raise ValueError("value must be positive")


parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--mode",
    "-m",
    type=str,
    choices=game_modes.SELECTOR_TO_MODE.keys(),
    default=game_modes.LetterToCodeMode.get_selector(),
    help="Selector of what is prompted",
)
parser.add_argument(
    "-n",
    type=positive_int,
    default=1,
    help="The length of sequences to guess",
)
args = parser.parse_args()

mode = game_modes.SELECTOR_TO_MODE[args.mode](args.n)

print("Selected mode:", args.mode)
print(mode.get_startup_message())
print("Press Ctrl+D or Ctrl+C to exit\n")
### CLI CONFIG END

# question loop
while True:
    prompt, expected_answer = mode.generate_next()
    # input loop
    while True:
        try:
            print(prompt, end=" ")
            answer = mode.get_normalized_input_tokens()
        except (KeyboardInterrupt, EOFError):
            # Handles Ctrl+C, Ctrl+D
            print()
            print("Total questions:", mode.generated_questions_count)
            print("Attempts:", mode.attempts_count)
            print("Correct attempts:", mode.correct_attempts_count)
            sys.exit()

        if not answer:
            continue

        mode.attempts_count += 1
        if answer == expected_answer:
            mode.correct_attempts_count += 1
            print("Correct!\n")
            break

        print("Wrong!")
