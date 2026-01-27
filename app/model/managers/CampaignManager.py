from injector import inject
from model.dao.ICampaignDAO import ICampaignDAO

class CampaignManager:
    @inject
    def __init__(self, campaign_dao: ICampaignDAO):
        self.__campaign_dao = campaign_dao

    def create_new_campaign(self, title: str, user_id: int):
        if not title:
            raise ValueError("Le titre ne peut pas être vide")
        self.__campaign_dao.create_campaign(title, user_id)

    def get_user_campaigns(self, user_id: int) -> list:
        result = []
        if user_id:
            result = self.__campaign_dao.get_campaigns_by_user(user_id)
        return result
    
    def delete_campaign(self, campaign_id: int, user_id: int):
        if campaign_id and user_id:
            self.__campaign_dao.delete_campaign(campaign_id, user_id)

    def get_campaign_subjects(self, campaign_id: int) -> list:
        result = []
        if campaign_id:
            result = self.__campaign_dao.get_subjects_by_campaign(campaign_id)
        return result

    def get_campaign_by_id(self, campaign_id: int):
        """
        Récupère les détails d'une campagne spécifique
        """
        result = None
        if campaign_id:
            result = self.__campaign_dao.get_campaign_by_id(campaign_id)
        return result
    
    def export_campaign_json(self, campaign_id: int):
        return self.__campaign_dao.get_full_campaign_data(campaign_id)
    
    def get_all_sources(self, user_id: int) -> list:
        """
        Récupère toutes les sources en fonction d'un user id
        
        :param self: Description
        :param user_id: Description
        :type user_id: int
        :return: liste de toutes les sources
        :rtype: list
        """
        return self.__campaign_dao.get_all_user_sources(user_id)
    
    def get_dashboard_data(self, user_id: int) -> dict:
        """
        Recupère les data a affiché dans le dashboard, cela comprends les cinq dernières campagnes,
        le nombres de source en fonction leur catégories et enfin le nombre d'entités en fonction de leur type
        
        :param self: Description
        :param user_id: Description
        :type user_id: int
        :return: dictionnaire contenant les dernieres camapagnes et les stats
        :rtype: dict
        """
        return {
            "last_campaigns": self.__campaign_dao.get_last_five_campaigns(user_id),
            "stats": self.__campaign_dao.get_user_stats_detailed(user_id)
        }
    
    def add_audit_log(self, user_id: int, username: str, action: str, campaign_name: str, target_details: str):
        """
        Relai les information au DAO
        
        :param self: Description
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
        self.__campaign_dao.add_audit_log(user_id, username, action, campaign_name, target_details)
    