class Relation:

    def __init__(self):
        self.__id = None
        self.__artifact_id = None
        self.__entity_id = None
        self.__context = None

    def get_id(self) -> int:
        """
        Récupère l'id d'une relation
        
        :param self: Description
        :return: l'id de la relation
        :rtype: int
        """
        return self.__id

    def set_id(self, id: int):
        """
        Définie l'id d'une relation
        
        :param self: Description
        """
        self.__id = id

    def get_artifact_id(self):
        """
        Récupère l'id d'un artefact
        
        :param self: Description
        :return: l'id de la l'artefact
        :rtype: int
        """
        return self.__artifact_id

    def set_artifact_id(self, artifact_id: int):
        """
        Définie l'id d'un artefact
        
        :param self: Description
        """
        self.__artifact_id = artifact_id

    def get_entity_id(self):
        """
        Récupère l'id d'une entite
        
        :param self: Description
        :return: l'id de l'entite
        :rtype: int
        """
        return self.__entity_id

    def set_entity_id(self, entity_id: int):
        """
        Définie l'id d'un entite
        
        :param self: Description
        """
        self.__entity_id = entity_id

    def get_context(self) -> str:
        """
        Récupère le contexte d'une relation
        
        :param self: Description
        :return: l'id de l'entite
        :rtype: int
        """
        return self.__context

    def set_context(self, context):
        """
        Définie le context d'une relation
        
        :param self: Description
        """
        self.__context = context