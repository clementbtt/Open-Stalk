import pytest 
import os
from injector import singleton
from app.server import app as flask_app 
import app.server as server_module 
from MockDatabase import MockDatabase
from app.model.dao.UserDAO import UserDAO
from app.model.dao.IDatabase import IDatabase
from app.model.dao.CampaignDAO import CampaignDAO
from app.server import injector

@pytest.fixture
def client(database): 
    # On force nos dao à utilisé notre MockDatabse
    injector.binder.bind(IDatabase, to=database, scope=singleton)
    server_module.campaign_controller._CampaignController__campaign_manager\
        ._CampaignManager__campaign_dao._CampaignDAO__database = database
    server_module.user_controller._UserController__user_manager\
        ._UserManager__userDAO._UserDAO__database = database
    server_module.scrapping_controller._ScrappingController__campaign_dao\
        ._CampaignDAO__database = database

    flask_app.config.update({
        'TESTING': True,
        'SECRET_KEY': "clé secrète pour les tests"      
    })
    
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def database():
    db = MockDatabase()
    path_sql = os.path.join(os.path.dirname(__file__), "bdd.sql")
    with open(path_sql, "r") as f:
        db.get_connection().executescript(f.read())
    yield db
    db.final_disconnect()


@pytest.fixture
def user_dao(database):
    database.execute_non_query("PRAGMA foreign_keys = OFF;")
    database.execute_non_query("DELETE FROM users;")
    database.execute_non_query("PRAGMA foreign_keys = ON;")
    return UserDAO(database)




@pytest.fixture
def campaign_dao(database):
    database.execute_non_query("PRAGMA foreign_keys = OFF;")
    database.execute_non_query("DELETE FROM campagnes;")
    database.execute_non_query("PRAGMA foreign_keys = ON;")
    return CampaignDAO(database)