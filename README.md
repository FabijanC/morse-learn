# Introduction

A CLI program for learning Morse code.

# Requirements

The program requires Python 3 to be installed.

# Installation

1. Clone this repository via `git clone`.
2. Install the dependencies with `pip install -r requirements.txt`
   - preferably create a virtual environment for this

# Usage

```
$ ./morse.py
V ...-
Correct!

X ...
Wrong
X -..-
Correct!

# Ctrl+D to exit
```

## Options

Select between letter-to-code and code-to-letter modes by providing a value to `-m` or `--mode`. By default, every prompt contains one symbol to convert. Modify this by specifying `-n <NUMBER>`.

See options with `./morse.py --help`.
