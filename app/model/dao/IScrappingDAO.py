from abc import ABC
from model.Artifact import Artifact
from model.Entity import Entity
from model.Relation import Relation


class IScrappingDAO(ABC):
    """
    Interface permettant la gestion des données de scrapping
    """

    def add_artifact(artifact: Artifact) -> int:
        """
        Ajoute un artefcat en bdd

        :param artifact: aretefact à ajouter
        :type artifact: Artifact
        :return: Renvoi l'id d' l'artefact ajouté
        :rtype: int
        """
        pass

    def add_entity(entity: Entity) -> int:
        """
        Ajoute une entité en bdd

        :param entity: Entité à ajouter
        :type entity: Entity
        :return: Renvoi l'i de l'entité ajoutée
        :rtype: int
        """
        pass

    def add_relation(relation: Relation):
        """
        Ajoute une relation en bdd

        :param relation: Relation à ajouter
        :type relation: Relation
        """
        pass

    def get_data_types() -> list[list[object]]:
        """
        Récupère tous les types d'entités (email, pseudo, instagram...)

        :return: Renvoi la liste contenant tous les types d'entité
        :rtype: list[list[object]]
        """
        pass
