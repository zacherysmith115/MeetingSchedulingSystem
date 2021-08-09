from passlib.context import CryptContext

from mss.User.UserModels import User
from mss.User.UserForms import EditAccountForm
class UserController:      

    db = None

    # create context with PBKDF2
    # private visibility
    __pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000  # -!- if wait time is too long reduce number of rounds -!-
    )


    def __init__(self) -> None:
        self.db = __import__('mss').db

    # Function to build edit account form 
    def buildCreateAccountForm(self, user : "User", form: "EditAccountForm") -> None:
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email

    # Function to try and update the database with the request changes
    def updateAccount(self, user : "User", form : "EditAccountForm") -> bool:
        try:
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.last_name.data
            user.password = form.password.data
            return True
        except:
            return False

    # encyrpt a given password
    def encryptPassword(self, password: "str") -> "str":
        return self.__pwd_context.hash(password)
    
    # verify a given password
    def verifyPassword(self, password: "str", hashed: "str") -> bool:
        return self.__pwd_context.verify(password, hashed)

