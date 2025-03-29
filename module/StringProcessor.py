class StringProcessor():
    def __init__(self):
        pass

    def prettyString(self,text):
        text = text.upper()
        retStr = str()
        index = 0
        foundLetterOrNumber = True
        foundComma = True
        while index < len(text):
            if text[index] >= '0' and text[index] <= '9' or text[index] >= 'A' and text[index] <= 'Z' or text[index] == '.':
                if not foundLetterOrNumber:
                    if not foundComma:
                        retStr = retStr + ' '
                foundLetterOrNumber = True
                foundComma = False
                retStr = retStr + text[index]
            elif text[index] == ',':
                foundLetterOrNumber = False
                if not foundComma:
                    foundComma = True
                    retStr = retStr + ", "
            else:
                foundLetterOrNumber = False
            index = index + 1
        return retStr.removesuffix(", ")
    
    def getWords(self,text):
        retSet = set({})
        word = str()
        index = 0
        foundLetterOrNumber = True
        foundComma = True
        while index < len(text):
            if text[index] >= '0' and text[index] <= '9' or text[index] >= 'A' and text[index] <= 'Z' or text[index] == '.':
                if not foundLetterOrNumber:
                    if not foundComma:
                        word = word + ' '
                foundLetterOrNumber = True
                foundComma = False
                word = word + text[index]
            elif text[index] == ',':
                foundLetterOrNumber = False
                if not foundComma:
                    foundComma = True
                    retSet.add(word)
                    word = ""
            else:
                foundLetterOrNumber = False
            index = index + 1
        retSet.add(word)
        return retSet