"""The data the program operates on."""

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
    "Z": "--..",
}

letters = letter2code.keys()
codes = letter2code.values()

_sorted_letters = sorted(letters)
assert len(letters) == len(set(letters))
assert len(letters) == 26
assert _sorted_letters[0] == "A"
assert _sorted_letters[-1] == "Z"
assert all(map(lambda code: all(map(lambda symbol: symbol in ".-", code)), codes))
assert len(set(codes)) == len(codes)
assert len(codes) == 26
