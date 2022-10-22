from playsound import playsound
import pyttsx3


engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty("rate",100)

volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)

voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)

def fromTextToMorse(name,StringInMorse):
    
    #read the file
    fileMorseCode = open("morseCode.txt","r").readlines()
    name = name.upper()

    for lettre in name:
        playsound(r'soundeLetters/'+lettre+'.wav')
        for line in fileMorseCode:
            if line[0] == lettre:
                line = line[2 : -1 : ] 
                StringInMorse += line
                StringInMorse += "   "

    StringInMorse += "/       "
    return StringInMorse

def menu():
    print("1- Text -> Corse code")
    print("2- Morse code -> Text")
    choise = input()

    if choise=='1':
        print("What's your name ?")
        Name = input()
        listOfNameSplited = Name.split()
        StringInMorse = ""

        for nameSplited in listOfNameSplited:
            StringInMorse = fromTextToMorse(nameSplited,StringInMorse)

        print(StringInMorse)

    elif choise=='2':
        print("What's your name ?")
        name = input()
        fromMorseToText(name)
    else:
        print("404")

def fromMorseToText(name):
    fileMorseCode = open("morseCode.txt","r").readlines()
    myName = ""
    ALLNameSplited = name.split("       ")

    for NameParts in ALLNameSplited:
        letters = NameParts.split("   ")
        for letter in letters:
            for line in fileMorseCode:
                if letter == line[2 : -1 : ]:

                    myName += line[0:1:]
        myName += "  "
        
    print(myName)
    engine.say(myName)
    engine.runAndWait()


#Main


choise = menu()