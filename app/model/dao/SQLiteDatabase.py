import sqlite3
from .IDatabase import IDatabase


class SQLiteDatabase(IDatabase):
    """
    Classe gérarant des intéractions avec une base de données SQLite
    """

    def __init__(self, dbname:str):
        """
        Constructeur de la classe
        """
        self.__db_name = dbname
        self.__connection = sqlite3.connect(dbname, check_same_thread=False)

    def connect(self):
        self.__connection = sqlite3.connect(self.__db_name, check_same_thread=False)
        self.__connection.execute("PRAGMA foreign_keys = ON") # Permet la suppression en cascade

    def disconnect(self):
        self.__connection.close()

    def execute_non_query(self, query: str, parameters: tuple[object] = ()):
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query, parameters)
            self.__connection.commit()
        except Exception as e:
            print(e)
            raise e

    def execute_query(
        self, query: str, parameters: tuple[object] = ()
    ) -> list[tuple[object]]:
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query, parameters)
            self.__connection.commit()
            return cursor.fetchall()
        except Exception as e:
            print(e)
            raise e
