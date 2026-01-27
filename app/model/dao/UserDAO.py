import bcrypt
from .IUserDAO import IUserDAO
from .IDatabase import IDatabase
from injector import inject
from ..User import User


class UserDAO(IUserDAO):
    '''
    DAO pour la gestion des utilisateurs
    '''

    @inject
    def __init__(self, database:IDatabase):
        '''
        Constructeur de la classe
        
        :param database: Instance de la bdd
        :type database: IDatabase
        '''
        self.__database = database

    def check_authentication(self, user: User)->bool:
        bdd_user = self.get_user_by_username(user.get_username())
        response = False
        if bdd_user != None:
            password = user.get_password()
            password_bytes = password.encode("utf-8")
            if bcrypt.checkpw(password_bytes, bdd_user.get_password()):
                response = True
        return response

    def get_user_by_username(self, username: str)->User:
        self.__database.connect()

        params = tuple([username])
        data = self.__database.execute_query("select * from users where username = (?)", params)
        user = None
        if data and len(data) > 0:
            user = User()
            user.set_id(data[0][0])
            user.set_username(data[0][1])
            user.set_password(data[0][2])
        self.__database.disconnect()
        return user

    def register(self, user: User):
        self.__database.connect()

        username = user.get_username()
        password = user.get_password()

        params = tuple([username, password])

        self.__database.execute_non_query("insert into users(username, password_hash) values (?, ?)", params)

        self.__database.disconnect()