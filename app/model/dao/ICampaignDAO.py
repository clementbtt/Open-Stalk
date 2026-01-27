from abc import ABC

class ICampaignDAO(ABC):
    def create_campaign(title: str, user_id: int):
        """
        Permet de créer une campagne avec l'id de l'utilisateur et un nom
        
        :param self: Description
        :param title: Description
        :type title: str
        :param user_id: Description
        :type user_id: int
        """
        pass

    def get_campaigns_by_user(user_id: int) -> list:
        """
        Permet de récupérer les campagnes en fonction de l'id de l'utilisateur
        
        :param self: Description
        :param user_id: Description
        :type user_id: int
        :return: une liste contenant les IDs et noms d'un campagnes
        :rtype: list
        """
        pass

    def delete_campaign(campaign_id: int, user_id: int):
        """
        Permet de supprimer une campagne en fonction d'un id de campagne et d'un id d'utilisateur
        
        :param self: Description
        :param campaign_id: Description
        :type campaign_id: int
        :param user_id: Description
        :type user_id: int
        """
        pass

    def add_subject(title: str, campaign_id: int) -> int:
        """
        Permet de récupérer l'id d'un sujet de recherche (pour les APIs) en fonction d'un titre et 
        d'un campagne id, s'il n'y a rien en base de donnée alors on le crée et on renvoie son id.

        
        :param self: Description
        :param title: Description
        :type title: str
        :param campaign_id: Description
        :type campaign_id: int
        :return: l'id d'un sujet de recherche
        :rtype: int
        """
        pass

    def add_source(type_source: int, url: str, campagne_id:int,  subject_id: int = None) -> int:
        """
        Permet de récupérer l'id d'une source en fonction d'un type, un url, un campagne id et un subject qui 
        est None par défaut (si la source n'est pas une API). S'il n'existe pas alors on le crée et on récupère son id
        
        :param self: Description
        :param type_source: Description
        :type type_source: int
        :param url: Description
        :type url: str
        :param campagne_id: Description
        :type campagne_id: int
        :param subject_id: Description
        :type subject_id: int
        :return: l'id d'une source
        :rtype: int
        """
        pass
    
    def get_campaign_by_id(campaign_id: int):
        """
        Renvoie toutes les éléments concernant d'une campagne en fonction de son id.
        
        :param self: Description
        :param campaign_id: Description
        :type campaign_id: int
        :return: un tuple si la campagne existe, sinon None
        :rtype: tuple | None
        """
        pass

    def get_subjects_by_campaign(campaign_id: int) -> list:
        """
        Renvoie les libelles d'un sujet de recherche en fonction d'un campagne id
        
        :param self: Description
        :param campaign_id: Description
        :type campaign_id: int
        :return: une liste contenant les libelles
        :rtype: list
        """
        pass

    def get_full_campaign_data(campaign_id: int) -> dict:
        """
        Récupère l'ensemble des données d'une campagne grâce à deux jointures

        :param campaign_id: L'identifiant de la campagne.
        :type campaign_id: int
        :return: Un dictionnaire contenant les 'metadata' (infos campagne) et les 'findings' (liste des entités trouvées par URL)
        :rtype: dict
        """
        pass

    def add_audit_log(user_id: int, username: str, action: str, campaign_name: str, target_details: str):
        """
        Enregistre les logs sur notre table
        
        :param user_id: Description
        :type user_id: int
        :param username: Description
        :type username: str
        :param action: Description
        :type action: str
        :param campaign_name: Description
        :type campaign_name: str
        :param target_details: Description
        :type target_details: str
        """
        pass


    