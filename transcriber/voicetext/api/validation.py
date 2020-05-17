import re
import logging


#TODO : convert to model based and add test cases

upper = "AÀÂBCÇDEÉÈÊFGHIÎJKLMNOÔPQRSTUVWXYZ"
lower = "aàâbcçdeéèêëfghiîïjklmnoôpqrstuùûvwxyz"
special_chars = "()'-?,.;:!"

loggerp = logging.getLogger("api-segment-post")

def validate(x):
    if charactercheck(x.replace(" ","")):
        if checkForWordCaps(x):
            if checkForSpaces(x):
                print("safe so far")
                return True
    
    return False
    
def charactercheck(x):
    loggerp.info("Character Check")
    validate_chars = upper+lower+special_chars
    for char in x:
        if not validate_chars.__contains__(char):
            loggerp.info("Character Check -- Failed")
            return False
    loggerp.info("Character Check -- Pass")
    return True

def checkForWordCaps(x):
    loggerp.info("Character Word Capitilization")
    x= x.strip()
    words = x.split(" ");
    words = [w for w in words if w]
    for word in words:
        if special_chars.__contains__(word):
            pass
        if upper.__contains__(word[:1]):
            if word[1:].islower() or word[1:].isupper():
                pass
            else:
                loggerp.info("Character Word Capitilization -- Failed")
                return False
    loggerp.info("Character Word Capitilization -- Pass")
    return True

def checkForSpaces(x):
    loggerp.info("Character spacing check")
    regex = r"^([A-Za-z]+ )+[A-Za-z]+$|^[A-Za-z]+$"
    if re.search(regex, x) == None:
        loggerp.info("Character spacing check -- Failed")
        return False
    loggerp.info("Character spacing check -- Pass")
    return True
        