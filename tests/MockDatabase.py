from app.model.dao.IDatabase import IDatabase
import os
import sqlite3

class MockDatabase(IDatabase):

    def __init__(self):
        """
        Constructeur de la classe
        """
        self.__connection = sqlite3.connect(":memory:", check_same_thread=False)
        self.__connection.execute("PRAGMA foreign_keys = ON")

    def connect(self):
        pass

    def disconnect(self):
        pass

    def final_disconnect(self):
        self.__connection.close()
    
    def get_connection(self):
        return self.__connection

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
    