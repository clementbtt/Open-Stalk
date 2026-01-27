from injector import Module, singleton

from model.dao.IUserDAO import IUserDAO
from model.dao.UserDAO import UserDAO
from model.dao.IDatabase import IDatabase
from model.dao.SQLiteDatabase import SQLiteDatabase
from model.dao.IScrappingDAO import IScrappingDAO
from model.dao.ScrappingDAO import ScrappingDAO
from model.dao.ICampaignDAO import ICampaignDAO
from model.dao.CampaignDAO import CampaignDAO
from pathlib import Path


class AppModule(Module):
    '''
    Classe permettant de gérer l'injection de dépendances
    '''

    def configure(self, binder):
        '''
        Configuration de l'injection de dépendances
        '''
        root = Path(__file__).resolve().parent.parent
        binder.bind(IUserDAO, to=UserDAO, scope=singleton)
        binder.bind(IDatabase, to=SQLiteDatabase(root / "app.db"), scope=singleton)
        binder.bind(IScrappingDAO, to=ScrappingDAO, scope=singleton)
        binder.bind(ICampaignDAO, to=CampaignDAO, scope=singleton)