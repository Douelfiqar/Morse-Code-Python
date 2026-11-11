"""Shared Morse code helpers used by CodeMorse.py and GiToMorseCOde.py.

Two Morse notations are understood:

* The notation of this project (the one in morseCode.txt): a dot is ".",
  a dash is "---", symbols are separated by 1 space, letters by 3 spaces
  and words by "/" or 5+ spaces.
      SOS  ->  ". . .   --- --- ---   . . .   /       "
* Standard notation: a dot is ".", a dash is "-", letters are separated by
  1 space and words by "/" or 2+ spaces.
      SOS  ->  "... --- ..."
"""
import os
import re
import unicodedata

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LETTER_GAP = "   "      # written after each letter
WORD_END = "/       "   # written after each word


def path(name):
    """Absolute path of a file in the project folder, so the scripts work from any directory."""
    return os.path.join(BASE_DIR, name)


def load_table(filename=None):
    """Read morseCode.txt into {char: code}, code in the project's notation."""
    table = {}
    with open(filename or path("morseCode.txt"), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\r\n")
            if len(line) < 3 or line[1] != " ":
                continue
            table[line[0]] = " ".join(line[2:].split())
    return table


TABLE = load_table()


def _to_standard_code(code):
    """'. ---' -> '.-'"""
    return "".join("-" if symbol == "---" else symbol for symbol in code.split())


_FROM_STANDARD = {_to_standard_code(code): char for char, code in TABLE.items()}


def normalize(text):
    """Upper-case and strip accents (é -> E) so names like 'José' can be encoded."""
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c)).upper()


def text_to_morse(text):
    """Return (morse in the project's notation, list of characters that have no Morse code)."""
    morse = ""
    unknown = []
    for word in normalize(text).split():
        for char in word:
            code = TABLE.get(char)
            if code is None:
                unknown.append(char)
                continue
            morse += code + LETTER_GAP
        morse += WORD_END
    return morse, unknown


def text_to_standard_morse(text):
    """Same as text_to_morse but in standard notation, e.g. '... --- ... / ..'."""
    words = []
    for word in normalize(text).split():
        codes = [_to_standard_code(TABLE[c]) for c in word if c in TABLE]
        if codes:
            words.append(" ".join(codes))
    return " / ".join(words)


_SYMBOL_FIXES = str.maketrans({"_": "-", "–": "-", "—": "-", "−": "-",
                               "·": ".", "•": "."})


def _is_project_notation(morse):
    tokens = morse.split()
    return bool(tokens) and all(t in (".", "---", "/") for t in tokens) and "   " in morse


def morse_to_text(morse):
    """Decode Morse in either notation. Return (text, list of codes that were not recognised)."""
    morse = morse.translate(_SYMBOL_FIXES).strip()
    if _is_project_notation(morse):
        words = re.split(r"\s*/\s*| {5,}", morse)
        split_letters = lambda w: [_to_standard_code(t) for t in re.split(r" {2,}", w) if t.strip()]
    else:
        words = re.split(r"\s*/\s*|\s{2,}", morse)
        split_letters = str.split

    decoded_words = []
    unknown = []
    for word in words:
        letters = []
        for code in split_letters(word.strip()):
            char = _FROM_STANDARD.get(code)
            if char is None:
                unknown.append(code)
                char = "?"
            letters.append(char)
        if letters:
            decoded_words.append("".join(letters))
    return " ".join(decoded_words), unknown
