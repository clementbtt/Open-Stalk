from abc import ABC
from ..User import User


class IUserDAO(ABC):
    """
    Interface permettant la gestion des données de l'utilisateur
    """

    def check_authentication(user: User) -> bool:
        """
        Vérifie les informations de connection de l'utilisateur

        :param user: Objet qui stocke les informations saisies par l'utilisateur
        :type user: User
        :return: True si les informations sont correctes, False sinon
        :rtype: bool
        """
        pass

    def get_user_by_username(username: str) -> User:
        """
        Récupère les données d'un utilisateur en fonction de son nom d'utilisateur

        :param username: Le nom d'utilisateur duquel on veut récupérer les informations
        :type username: str
        :return: L'utilisateur
        :rtype: User
        """
        pass

    def register(user: User):
        """
        Enregistre un nouvel utilisateur en base de données

        :param user: Utilisateur à enregister
        :type user: User
        """
        pass
