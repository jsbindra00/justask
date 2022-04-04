import hashlib
import re

class Utility:

    # https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/
    def IsEmailAddress(email):
        #return True
        return re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email)

    # https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
    def ContainsANumber(string):
        #return True
        return any(char.isdigit() for char in string)
    
    # https://stackoverflow.com/questions/45381206/how-to-test-if-a-string-has-capital-letters
    def ContainsACapital(string):
        #return True
        return any(char.isupper() for char in string)

    def ContainsALower(string):
        #return True
        return any(char for char in string if char.islower())
    
    def LengthIsAtleastN(N, string):
        #return True
        return N <= len(string)
    
    def IsStrongPassword(string):
        #return True
        return Utility.LengthIsAtleastN(8, string) and Utility.ContainsANumber(string) and Utility.ContainsALower(string) and Utility.ContainsACapital(string)

    def EncryptSHA256(string):
        return hashlib.sha256(string.encode()).hexdigest()
