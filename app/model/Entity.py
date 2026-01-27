class Entity:

    def __init__(self):
        self.__id = None
        self.__element = None
        self.__type_osint = None

    def get_id(self) -> int:
        """
        Récupère l'id de l'entité

        :return: l'id de l'entité
        :rtype: int
        """
        return self.__id

    def set_id(self, id: int):
        """
        Modifie l'id de l'entité

        :param id: nouvelle valeur de l'id
        :type id: int
        """
        self.__id = id

    def get_element(self) -> str:
        """
        Récupère l'élément de l'entité

        :return: Renvoi l'élément de l'entité
        :rtype: str
        """
        return self.__element

    def set_element(self, element: str):
        """
        Modifie l'élément de l'entité

        :param element: Nouvelle valeur de l'élément
        :type element: str
        """
        self.__element = element

    def get_type_osint(self) -> int:
        """
        Récupère le type de scrapping

        :return: le type de scrapping
        :rtype: int
        """
        return self.__type_osint

    def set_type_osint(self, type_osint: int):
        """
        Modifie le type de scrapping

        :param type_osint: Nouvelle valeur du type de scrapping
        :type type_osint: int
        """
        self.__type_osint = type_osint
