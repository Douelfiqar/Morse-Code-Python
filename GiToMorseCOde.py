def fromTextToMorse(name,StringInMorse):

    #read the file
    fileMorseCode = open("morseCode.txt","r").readlines()
    name = name.upper()

    for lettre in name:
        for line in fileMorseCode:
            if line[0] == lettre:
                line = line[2 : -1 : ] 
                StringInMorse += line
                StringInMorse += "   "
    #loop unitil i findx the char
    StringInMorse += "/       "
    return StringInMorse


def LstToMorse():
    GiFile = open("ListLstGi.txt","r").readlines()
    GiMorseFill = open("FullNameInMorseCode.txt",'w')
    for FullName in GiFile:
        FullName = FullName.upper()
        listOfNameSplited = FullName.split()
        StringInMorse = ""

        for nameSplited in listOfNameSplited:
            StringInMorse = fromTextToMorse(nameSplited,StringInMorse)
            
        FullName = FullName.rstrip()
        GiMorseFill.write(StringInMorse+'\n\n\n')


def fromMorseToText():
    fileMorseCode = open("OnlyNameMorse.txt","r").readlines()
    fromMorseToText = open("fromMorseToText.txt",'w')
    Dicionaire = open("morseCode.txt","r").readlines()

    for line in fileMorseCode:
        myName = "" 
        lineSplited = line.split("       ")
        for name in lineSplited:
            nameSplited = name.split("   ")
            for letter in nameSplited:
                for Dic in Dicionaire:
                    if letter == Dic[2:-1:]:
                        myName += Dic[0:1:]
            myName += " "
        fromMorseToText.write(myName+'\n')
#LstToMorse()
fromMorseToText()