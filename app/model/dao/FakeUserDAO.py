from model.User import User
from model.dao.IUserDAO import IUserDAO

class FakeUserDAO(IUserDAO):

    def __init__(self):
        self.__users = {
            "cbt": "password",
            "toto": "tata"
        }

    def check_authentication(self, user:User)->bool:
        valid = False
        if user.get_username() in self.__users.keys():
            username = user.get_username()
            password = user.get_password()
            if self.__users[username] == password:
                valid = True
        return valid