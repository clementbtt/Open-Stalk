class User:
    '''
    Représente un utilisateur
    '''

    def __init__(self):
        self.__id = None
        self.__username = None
        self.__password = None

    def get_id(self)->int:
        '''
        Récupère l'id de l'utilisateur

        :return: L'id de l'utilisateur
        :rtype: int
        '''
        return self.__id
    
    def get_username(self)->str:
        '''
        Récupère le nom de l'utilisateur

        :return: le login de l'utilisateur
        :rtype: str
        '''
        return self.__username
    
    def get_password(self)->str:
        '''
        Récupère le mot de passe de l'utilisateur

        :return: le mot de passe de l'utilisateur
        :rtype: str
        '''
        return self.__password


    def set_id(self, id:int):
        '''
        Modifie l'id de l'utilisateur
        
        :param id: Nouvel
        :type id: int
        '''
        self.__id = id
    
    def set_username(self, username:str):
        '''
        Modifie le login de l'utilisateur
        
        :param username: Nouveau nom d'utilisateur
        :type username: str
        '''
        self.__username = username
    
    def set_password(self, password:str):
        '''
        Modifie le mot de passe de l'utilisateur

        :param password: Nouveau mot de passe
        :type password: str
        '''
        self.__password = password