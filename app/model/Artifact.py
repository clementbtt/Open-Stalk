class Artifact:
    """
    Représente un artéfact
    """

    def __init__(self):
        self.__id = None
        self.__source_id = None
        self.__date = None
        self.__url = None
        self.__content = None
        self.__contenu_hash = None
        self.__status_code = None
        self.__headers = None

    def get_id(self) -> int:
        """
        Récupère l'id de l'artefcat

        :return: L'id de l'artefact
        :rtype: int
        """
        return self.__id

    def set_id(self, id: int):
        """
        Modifie l'id de l'artefact

        :param id: Nouvelle valeur de l'id
        :type id: int
        """
        self.__id = id

    def get_source_id(self) -> int:
        """
        Récupère l'id de la source de l'artefact

        :return: Id de la source
        :rtype: int
        """
        return self.__source_id

    def set_source_id(self, source_id: int):
        """
        Modifie la source de l'id

        :param source_id: Nouvelle valeur de l'id de la source
        :type source_id: int
        """
        self.__source_id = source_id

    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date

    def get_url(self) -> str:
        """
        Récupère l'url de l'artefact

        :return: L'url de l'artefact
        :rtype: str
        """
        return self.__url

    def set_url(self, url: str):
        """
        Modifie la valeur de l'url

        :param url: Nouvelle valeur de l'url
        :type url: str
        """
        self.__url = url

    def get_content(self) -> str:
        """
        Renvoi le contenu de l'artefact

        :param self: Description
        :return: Description
        :rtype: str
        """
        return self.__content

    def set_content(self, content: str):
        """
        Modifie le contenu de l'artefact

        :param content: Nouvelle valeur du contenu
        :type content: str
        """
        self.__content = content

    def set_contenu_hash(self, contenu_hash: str):
        """
        Modifie le hash de l'artefact

        :param contenu_hash: Nouvelle valeur du hash
        :type contenu_hash: str
        """
        self.__contenu_hash = contenu_hash

    def get_contenu_hash(self) -> str:
        """
        Renvoi le has de l'artefact

        :return: Le hash de l'artefact
        :rtype: str
        """
        return self.__contenu_hash

    def set_status_code(self, status_code: int):
        """
        Modifie le code de réponse de l'artefact

        :param status_code: Nouvelle valeur du code de réponse
        :type status_code: int
        """
        self.__status_code = status_code

    def get_status_code(self) -> int:
        """
        Renvoi le code de réponse de l'artefact

        :return: Le code de réponse
        :rtype: int
        """
        return self.__status_code

    def set_headers(self, headers: str):
        """
        Modifie l'en-tête de l'artefact

        :param headers: Nouvelle en-tête
        :type headers: str
        """
        self.__headers = headers

    def get_headers(self) -> str:
        """
        Renvoi l'en-tête de l'artefact

        :return: L'en-tête de l'artefact
        :rtype: str
        """
        return self.__headers
