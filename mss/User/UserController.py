

from mss.User.UserModels import User, Client
from mss.User.UserForms import EditAccountForm



class UserController:      

    db = None

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


    

