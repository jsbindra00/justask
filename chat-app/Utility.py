import re
import hashlib
class Utility:
    def IsEmailAddress(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def ContainsANumber(string):
        return True
    
    def LengthIsAtleastN(N, string):
        return True
    
    def IsStrongPassword(string):
        return Utility.LengthIsAtleastN(10, string) and Utility.ContainsANumber(string)

    def EncryptSHA256(string):
        return hashlib.sha256(string.encode()).hexdigest()
