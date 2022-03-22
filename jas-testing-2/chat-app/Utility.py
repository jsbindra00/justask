import re

class Utility:
    def IsEmailAddress(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def ContainsANumber(string):
        return True
    
    def LengthIsAtleastN(N, string):
        return True
    
    

    def IsStrongPassword(string):
        return Utility.LengthIsAtleastN(10, string) and Utility.ContainsANumber(string)