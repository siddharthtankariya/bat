import re

#TODO : convert to model based and add test cases

upper = "AÀÂBCÇDEÉÈÊFGHIÎJKLMNOÔPQRSTUVWXYZ"
lower = "aàâbcçdeéèêëfghiîïjklmnoôpqrstuùûvwxyz"
special_chars = "()'-?,.;:!"


def validate(x):
    if charactercheck(x.replace(" ","")):
        if checkForWordCaps(x):
            if checkForSpaces(x):
                print("safe so far")
                return True
    
    return False
    
def charactercheck(x):
    validate_chars = upper+lower+special_chars
    for char in x:
        if not validate_chars.__contains__(char):
            return False
    return True

def checkForWordCaps(x):
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
                return False
    return True

def checkForSpaces(x):
    regex = r"^([A-Za-z]+ )+[A-Za-z]+$|^[A-Za-z]+$"
    if re.search(regex, x) == None:
        return False
    return True
        