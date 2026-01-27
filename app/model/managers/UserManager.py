from injector import inject
from werkzeug.security import generate_password_hash
import bcrypt
import hashlib
from ..dao.IUserDAO import IUserDAO
from ..User import User

class UserManager:
    '''
    Manager des utilisateurs faisant le lien entre le controller et le dao
    '''

    @inject
    def __init__(self, userDAO: IUserDAO):
        self.__userDAO = userDAO

    def check_authentication(self, username:str, password: str)->bool:
        '''
        Vérifie les informations de connexion de l'utilisateur
        
        :param username: nom d'utilisateur saisi
        :type username: str
        :param password: mot de passe saisi 
        :type password: str
        :return: True si lmes informations sont correctes, False sinon
        :rtype: bool
        '''
        valid = False
        try:
            user = User()
            user.set_username(username)
            user.set_password(password)
            valid = self.__userDAO.check_authentication(user)
        except:
            raise Exception("Erreur lors de l'authentification !")
        return valid
    
    def register(self, username:str, password: str):
        '''
        Inscrit un nouvel utilisateur
        
        :param username: nom d'utilisateur 
        :type username: str
        :param password: mot de passe
        :type password: str
        '''
        user = User()
        try:
            user.set_username(username)
            password_bytes = password.encode("utf-8")
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password_bytes, salt)
            user.set_password(hashed_password)
            self.__userDAO.register(user)
        except:
            raise Exception("Erreur lors de l'inscription !")
        
    def get_user_id_from_username(self, username: str)->int:
        '''
        Récupère l'id d'un utilisateur à partir de son pseudo
        
        :param username: Pseudo de l'utilisateur en question
        :type username: str
        :return: L'id de l'utilisateur
        :rtype: int
        '''
        user = self.__userDAO.get_user_by_username(username)
        return user.get_id()