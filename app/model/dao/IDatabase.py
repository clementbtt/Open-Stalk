from abc import ABC


class IDatabase(ABC):
    """
    Interface représentant une base de données
    """

    def connect():
        """
        Etablit la connexion à la bdd
        """
        pass

    def disconnect():
        """
        Ferme la connexion à la bdd
        """
        pass

    def execute_query(query: str, parameters: tuple[object] = ()) -> list[list[object]]:
        """
        Exécute une requête SQL retournant des résultats

        :param query: Requête à exécuter
        :type query: str
        :param parametters: Paramètres à inclure à la requête
        :type parametters: tuple[object]
        :return: La liste des lignes retournées par l'exécution de la requête
        :rtype: list[list[object]]
        """
        pass

    def execute_non_query(query: str, parameters: tuple[object] = ()):
        """
        Exécute une requête SQL ne retournant pas de résultats

        :param query: Requête à exécuter
        :type query: str
        :param parameters: Paramètres à inclure à la requête
        :type parameters: tuple[object]
        """
        pass
