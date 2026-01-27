from .IScrappingDAO import IScrappingDAO
from .IDatabase import IDatabase
from model.Artifact import Artifact
from model.Entity import Entity
from model.Relation import Relation
from injector import inject


class ScrappingDAO(IScrappingDAO):

    @inject
    def __init__(self, database: IDatabase):
        """
        Constructeur de la classe

        :param database: Instance de la bdd
        :type database: IDatabase
        """
        self.__database = database

    def add_artifact(self, artifact: Artifact) -> int:
        self.__database.connect()
        check_query = "SELECT artefact_id FROM artefacts WHERE contenu_hash = ?;"
        existe = self.__database.execute_query(
            check_query, (artifact.get_contenu_hash(),)
        )

        if existe:
            id = existe[0][0]
        else:
            params = (
                artifact.get_source_id(),
                artifact.get_url(),
                artifact.get_content(),
                artifact.get_contenu_hash(),
                artifact.get_status_code(),
                artifact.get_headers(),
            )
            self.__database.execute_non_query(
                "INSERT INTO artefacts (source_id, url, contenu_brut, contenu_hash, status_code, headers) VALUES (?, ?, ?, ?, ?, ?);",
                params,
            )
            id = self.__database.execute_query("SELECT last_insert_rowid();")[0][0]
        self.__database.disconnect()
        return id

    def add_entity(self, entity: Entity) -> int:
        self.__database.connect()
        element = entity.get_element()
        type_id = entity.get_type_osint()
        params = (entity.get_element(), entity.get_type_osint())
        self.__database.execute_non_query(
            "insert or ignore into entites (element, type_osint_id) values (?,?);",
            params,
        )
        id = self.__database.execute_query(
            "SELECT entite_id FROM entites WHERE element = ? AND type_osint_id = ?;",
            (element, type_id),
        )[0][0]
        self.__database.disconnect()
        return id

    def add_relation(self, relation: Relation):
        self.__database.connect()
        art_id = relation.get_artifact_id()
        ent_id = relation.get_entity_id()
        contexte = relation.get_context()

        # On verifie d'abord si la meme relation existe deja
        check_query = (
            "SELECT relation_id FROM relations WHERE artefact_id = ? AND entite_id = ? AND contexte_extrait = ?;"
        )
        existe = self.__database.execute_query(check_query, (art_id, ent_id, contexte))
        if not existe:
            params = (art_id, ent_id, contexte)
            self.__database.execute_non_query(
                "insert into relations (artefact_id, entite_id, contexte_extrait) VALUES (?,?,?);",
                params,
            )
        self.__database.disconnect()

    def get_data_types(self) -> list[list[object]]:
        self.__database.connect()
        types = self.__database.execute_query("select * from types_entites;")
        self.__database.disconnect()
        return types
