class Campaign:
    """
    Représente une campagne de recherche
    """
    def __init__(self):
        self.__id = None
        self.__title = None
        self.__owner_id = None

    def get_id(self) -> int:
        """
        Récupère l'id d'une campagne
        
        :param self: Description
        :return: l'id de la campagne
        :rtype: int
        """
        return self.__id

    def set_id(self, id: int):
        """
        Définie l'id d'une campagne
        
        :param self: Description
        """
        self.__id = id

    def get_title(self) -> str:
        """
        Récupère le titre d'une campagne
        
        :param self: Description
        :return: le titre de la camapgne
        :rtype: str
        """
        return self.__title

    def set_title(self, title: str):
        """
        Définie le titre d'une campagne
        
        :param self: Description
        """
        self.__title = title

    def get_owner_id(self) -> int:
        """
        Récupère le propriétaire d'une campagne
        
        :param self: Description
        :return: l'id du propriétaire de la camapgne
        :rtype: int
        """
        return self.__owner_id

    def set_owner_id(self, owner_id: int):
        """
        Définie le propriétaire d'une campagne
        
        :param self: Description
        """
        self.__owner_id = owner_id