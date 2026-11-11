from morse_utils import morse_to_text, path, text_to_morse


def LstToMorse():
    """ListLstGi.txt (one name per line) -> FullNameInMorseCode.txt (name followed by its Morse code)."""
    with open(path("ListLstGi.txt"), encoding="utf-8") as names, \
            open(path("FullNameInMorseCode.txt"), "w", encoding="utf-8") as output:
        for full_name in names:
            full_name = full_name.strip().upper()
            if not full_name:
                continue
            morse, unknown = text_to_morse(full_name)
            if unknown:
                print(f"{full_name}: skipped characters without Morse code: {' '.join(unknown)}")
            output.write(full_name + "   " + morse + "\n\n\n")


def fromMorseToText():
    """OnlyNameMorse.txt (one Morse name per line) -> fromMorseToText.txt (decoded names)."""
    with open(path("OnlyNameMorse.txt"), encoding="utf-8") as morse_names, \
            open(path("fromMorseToText.txt"), "w", encoding="utf-8") as output:
        for line in morse_names:
            if not line.strip():
                continue
            name, unknown = morse_to_text(line)
            if unknown:
                print(f"{name}: unknown Morse code: {' | '.join(unknown)}")
            output.write(name + "\n")


if __name__ == "__main__":
    LstToMorse()
    fromMorseToText()
