from app.model.User import User

def test_add_campaign(campaign_dao, database, user_dao):
    user = User()
    user.set_username("clément")
    user.set_password("password")
    user_dao.register(user) # inscription du propriétaire de la campagne
    id = user_dao.get_user_by_username("clément").get_id() # récupération de l'id 
    assert get_length_of_campaigns(database) == 0
    titre = "Campagne numéro 1"
    campaign_dao.create_campaign(titre, id)
    assert get_length_of_campaigns(database) == 1

def test_get_campaigns_by_user(campaign_dao, user_dao):
    user = User()
    user.set_username("clément")
    user.set_password("password")
    user_dao.register(user) # inscription du propriétaire de la campagne
    id = user_dao.get_user_by_username("clément").get_id() # récupération de l'id 

    titre = "Campagne numéro 1"
    campaign_dao.create_campaign(titre, id)

    titre = "Campagne numéro 2"
    campaign_dao.create_campaign(titre, id)

    titre = "Campagne numéro 3"
    campaign_dao.create_campaign(titre, id)
    assert len(campaign_dao.get_campaigns_by_user(id)) == 3


def test_delete_campaign(campaign_dao, user_dao, database):
    user = User()
    user.set_username("clément")
    user.set_password("password")
    user_dao.register(user) # inscription du propriétaire de la campagne
    id = user_dao.get_user_by_username("clément").get_id() # récupération de l'id 

    titre = "Campagne numéro 1"
    campaign_dao.create_campaign(titre, id)
    assert get_length_of_campaigns(database) == 1

    campaign_id = campaign_dao.get_campaigns_by_user(id)[0][0]
    campaign_dao.delete_campaign(campaign_id, id)
    assert get_length_of_campaigns(database) == 0


def get_length_of_campaigns(database):
    database.connect()
    campaign = database.execute_query("select count(*) from campagnes;")
    database.disconnect()
    return campaign[0][0]