import os

from morse_utils import morse_to_text, normalize, path, text_to_morse, text_to_standard_morse

# Sound and speech are optional: the converter still works if they are missing or broken.
try:
    from playsound import playsound
except ImportError:
    playsound = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


def make_engine():
    if pyttsx3 is None:
        return None
    try:
        engine = pyttsx3.init()
    except Exception as error:
        print(f"(text-to-speech unavailable: {error})")
        return None
    engine.setProperty("rate", 100)
    engine.setProperty("volume", 1.0)
    voices = engine.getProperty("voices")
    if len(voices) > 1:
        engine.setProperty("voice", voices[1].id)
    return engine


def play_letters(text):
    """Play soundeLetters/<letter>.wav for each letter that has a sound file."""
    if playsound is None:
        return
    for char in normalize(text):
        wav = path(os.path.join("soundeLetters", char + ".wav"))
        if not os.path.exists(wav):
            continue
        try:
            playsound(wav)
        except Exception as error:
            print(f"(could not play sound: {error})")
            return


def fromTextToMorse(text):
    morse, unknown = text_to_morse(text)
    play_letters(text)
    print(morse)
    print("Standard notation:", text_to_standard_morse(text))
    if unknown:
        print("Skipped (no Morse code):", " ".join(sorted(set(unknown))))
    return morse


def fromMorseToText(morse):
    text, unknown = morse_to_text(morse)
    print(text)
    if unknown:
        print("Unknown Morse code (shown as ?):", " | ".join(unknown))
    engine = make_engine()
    if engine and text:
        engine.say(text)
        engine.runAndWait()
    return text


def menu():
    print("1- Text -> Morse code")
    print("2- Morse code -> Text")
    choice = input().strip()

    if choice == "1":
        print("What's your name ?")
        fromTextToMorse(input())
    elif choice == "2":
        print("Enter the Morse code, for example '... --- ...' or '. . .   --- --- ---   . . .'")
        fromMorseToText(input())
    else:
        print("Invalid choice, type 1 or 2.")


if __name__ == "__main__":
    menu()
