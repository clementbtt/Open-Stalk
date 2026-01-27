import requests
import json
from model.dao.IScrappingDAO import IScrappingDAO
from model.Artifact import Artifact
from model.Entity import Entity
from model.Relation import Relation
from injector import inject
import os
import hashlib


class GithubScrappingManager:
    """
    Manager des opérations de scrapping github
    """

    @inject
    def __init__(self, scrappingDAO: IScrappingDAO):
        self.__scrappingDAO = scrappingDAO

    def process(self, input_value: str, source_id):
        """ """
        # 1. Scraping Utilisateur
        data_user, meta_donne = self.scraping_user(input_value)

        if data_user and data_user.get("login"):
            artifact = Artifact()
            artifact.set_source_id(source_id)
            artifact.set_url(f"https://api.github.com/users/{input_value}")
            artifact.set_content(json.dumps(data_user))
            

            artifact.set_content(meta_donne["contenu_brut"]) 
            artifact.set_contenu_hash(meta_donne["contenu_hash"])   
            artifact.set_status_code(meta_donne["status_code"])
            artifact.set_headers(meta_donne["headers"])

            id = self.__scrappingDAO.add_artifact(artifact)
            artifact.set_id(id)

            # Email
            email = data_user.get("email")
            if email:
                entity = Entity()
                entity.set_element(str(email))
                entity.set_type_osint(1)
                id = self.__scrappingDAO.add_entity(entity)
                entity.set_id(id)

                relation = Relation()
                relation.set_artifact_id(artifact.get_id())
                relation.set_entity_id(entity.get_id())
                relation.set_context("Email profil GitHub")
                self.__scrappingDAO.add_relation(relation)

            # Blog
            blog = data_user.get("blog")
            if blog:
                entity = Entity()
                entity.set_element(str(blog))
                entity.set_type_osint(5)
                id = self.__scrappingDAO.add_entity(entity)
                entity.set_id(id)

                relation = Relation()
                relation.set_artifact_id(artifact.get_id())
                relation.set_entity_id(entity.get_id())
                relation.set_context("Site web profil GitHub")
                self.__scrappingDAO.add_relation(relation)

            # Followers
            for follower in data_user.get("followers_list", []):
                entity = Entity()
                entity.set_element(str(follower))
                entity.set_type_osint(2)
                id = self.__scrappingDAO.add_entity(entity)
                entity.set_id(id)

                relation = Relation()
                relation.set_artifact_id(artifact.get_id())
                relation.set_entity_id(entity.get_id())
                relation.set_context(f"Follower de {input_value}")
                self.__scrappingDAO.add_relation(relation)

            # Following
            for following in data_user.get("following_list", []):
                entity = Entity()
                entity.set_element(str(following))
                entity.set_type_osint(2)
                id = self.__scrappingDAO.add_entity(entity)
                entity.set_id(id)

                relation = Relation()
                relation.set_artifact_id(artifact.get_id())
                relation.set_entity_id(entity.get_id())
                relation.set_context(f"Suivi par {input_value}")
                self.__scrappingDAO.add_relation(relation)

        # 2. Scraping Repo
        data_repo, meta_donne = self.scraping_repo(input_value)

        if data_repo and data_repo.get("name"):
            artifact = Artifact()
            artifact.set_source_id(source_id)
            artifact.set_url(
                f"https://api.github.com/search/repositories?q={input_value}"
            )
            artifact.set_content(json.dumps(data_repo))

            artifact.set_content(meta_donne["contenu_brut"]) 
            artifact.set_contenu_hash(meta_donne["contenu_hash"])   
            artifact.set_status_code(meta_donne["status_code"])
            artifact.set_headers(meta_donne["headers"])
            try:
                id = self.__scrappingDAO.add_artifact(artifact)
                artifact.set_id(id)
            except TypeError as e:
                print(e)

            owner = data_repo.get("owner_login")
            if owner:
                entity = Entity()
                entity.set_element(str(owner))
                entity.set_type_osint(2)
                id = self.__scrappingDAO.add_entity(entity)
                entity.set_id(id)

                relation = Relation()
                relation.set_artifact_id(artifact.get_id())
                relation.set_entity_id(entity.get_id())
                relation.set_context("Propriétaire du repo")
                self.__scrappingDAO.add_relation(relation)

            for contrib in data_repo.get("contributors_list", []):
                entity = Entity()
                entity.set_element(str(contrib))
                entity.set_type_osint(2)
                id = self.__scrappingDAO.add_entity(entity)
                entity.set_id(id)

                relation = Relation()
                relation.set_artifact_id(artifact.get_id())
                relation.set_entity_id(entity.get_id())
                relation.set_context(f"Contributeur du repo {input_value}")
                self.__scrappingDAO.add_relation(relation)

        # 3. Scraping Organisation
        data_org, meta_donne = self.scraping_entity(input_value)
        if data_org and data_org.get("login"):
            artifact = Artifact()
            artifact.set_source_id(source_id)
            artifact.set_url(f"https://api.github.com/orgs/{input_value}")
            artifact.set_content(json.dumps(data_org))

            artifact.set_content(meta_donne["contenu_brut"]) 
            artifact.set_contenu_hash(meta_donne["contenu_hash"])   
            artifact.set_status_code(meta_donne["status_code"])
            artifact.set_headers(meta_donne["headers"])

            id = self.__scrappingDAO.add_artifact(artifact)
            artifact.set_id(id)

            org_email = data_org.get("email")
            if org_email:
                entity = Entity()
                entity.set_element(str(org_email))
                entity.set_type_osint(1)
                id = self.__scrappingDAO.add_entity(entity)
                entity.set_id(id)

                relation = Relation()
                relation.set_artifact_id(artifact.get_id())
                relation.set_entity_id(entity.get_id())
                relation.set_context("Email organisation")
                self.__scrappingDAO.add_relation(relation)

            org_blog = data_org.get("blog")
            if org_blog:
                entity = Entity()
                entity.set_element(str(org_blog))
                entity.set_type_osint(5)
                id = self.__scrappingDAO.add_entity(entity)
                entity.set_id(id)

                relation = Relation()
                relation.set_artifact_id(artifact.get_id())
                relation.set_entity_id(entity.get_id())
                relation.set_context("Site web organisation")
                self.__scrappingDAO.add_relation(relation)

            for member in data_org.get("members_list", []):
                entity = Entity()
                entity.set_element(str(member))
                entity.set_type_osint(2)
                id = self.__scrappingDAO.add_entity(entity)
                entity.set_id(id)

                relation = Relation()
                relation.set_artifact_id(artifact.get_id())
                relation.set_entity_id(entity.get_id())
                relation.set_context(f"Membre de l'organisation {input_value}")
                self.__scrappingDAO.add_relation(relation)

    def scraping_user(self, username):
        """
        Fonction qui prend en paramètre un username et retourne un dictionnaire concernant les informations qu'on a trouvé avec l'api git
        Chaque data.get est vérifié dans un if car les fonctions scraping_user, scraping_repo et scraping_entity sont appelées
        en même temps lorsque la source est github.Cela permet d'eviter de générer une erreur si le dictionnaire existe pas.
        """
        api_url = f"https://api.github.com/users/{username}"
        api_response = requests.get(api_url, headers=self.get_request_header())
        print("status user:", api_response.status_code)
        data = api_response.json()
        contenu_brut = api_response.text
        content_hash = hashlib.sha256(contenu_brut.encode('utf-8')).hexdigest()

        dico_user = {}
        meta_donne = {}

        meta_donne["contenu_brut"] = contenu_brut
        meta_donne["status_code"] = api_response.status_code
        meta_donne["headers"] = json.dumps(dict(api_response.headers))
        meta_donne["contenu_hash"] = content_hash


        dico_user["login"] = data.get("login")
        dico_user["email"] = data.get("email")
        dico_user["blog"] = data.get("blog")

        # Récupération des URL pour les listes
        followers_url = data.get("followers_url")
        following_url = data.get("following_url")

        # Liste des Followers
        if followers_url:
            api_response = requests.get(
                followers_url, headers=self.get_request_header()
            )
            print("status followers:", api_response.status_code)
            if api_response.status_code == 200:
                followers_data = api_response.json()
                tableau_followers = []
                for item in followers_data:
                    tableau_followers.append(item.get("login"))
                dico_user["followers_list"] = tableau_followers

        # Liste des Following
        if following_url:
            url_following_list = following_url.replace("{/other_user}", "")
            api_response = requests.get(
                url_following_list, headers=self.get_request_header()
            )
            print("status following:", api_response.status_code)
            if api_response.status_code == 200:
                following_data = api_response.json()
                tableau_following = []
                for item in following_data:
                    tableau_following.append(item.get("login"))
                dico_user["following_list"] = tableau_following

        return dico_user, meta_donne

    def get_request_header(self) -> dict:
        return {
            "User-Agent": "request",
            "Authorization": f"token {os.environ.get('GITHUB_KEY')}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def scraping_repo(self, repo_name):
        """
        Fonction qui prend en paramètre un repo et retourne un dictionnaire concernant les informations qu'on a trouvé avec l'api git
        Chaque data.get est vérifié dans un if car les fonctions scraping_user, scraping_repo et scraping_entity sont appelées
        en même temps lorsque la source est github.Cela permet d'eviter de générer une erreur si le dictionnaire existe pas.
        """
        search_api_url = f"https://api.github.com/search/repositories?q={repo_name}"
        api_response = requests.get(search_api_url, headers=self.get_request_header())
        print("status search repo:", api_response.status_code)
        search_data = api_response.json()
        contenu_brut = api_response.text
        content_hash = hashlib.sha256(contenu_brut.encode('utf-8')).hexdigest()

        dico_repo = {}
        meta_donne = {}

        meta_donne["contenu_brut"] = contenu_brut
        meta_donne["status_code"] = api_response.status_code
        meta_donne["headers"] = json.dumps(dict(api_response.headers))
        meta_donne["contenu_hash"] = content_hash

        # Vérification si un résultat existe
        if search_data.get("items"):
            repo_to_analyze = search_data["items"][0]
            data = repo_to_analyze

            dico_repo["name"] = data.get("name")
            dico_repo["owner_login"] = data.get("owner", {}).get("login")
            dico_repo["contributors_url"] = data.get("contributors_url")

            # Récupération de la liste des contributeurs
            if dico_repo.get("contributors_url"):
                api_response_contrib = requests.get(
                    dico_repo["contributors_url"], headers=self.get_request_header()
                )
                print("status contributors:", api_response_contrib.status_code)
                if api_response_contrib.status_code == 200:
                    contributors_data = api_response_contrib.json()
                    tableau_contributors = []
                    for contributor in contributors_data:
                        tableau_contributors.append(contributor.get("login"))
                    dico_repo["contributors_list"] = tableau_contributors

        return dico_repo, meta_donne

    def scraping_entity(self, entity_name):
        """
        Fonction qui prend en paramètre une entité et retourne un dictionnaire concernant les informations qu'on a trouvé avec l'api git
        Chaque data.get est vérifié dans un if car les fonctions scraping_user, scraping_repo et scraping_entity sont appelées
        en même temps lorsque la source est github.Cela permet d'eviter de générer une erreur si le dictionnaire existe pas.
        """
        api_url = f"https://api.github.com/orgs/{entity_name}"
        api_response = requests.get(api_url, headers=self.get_request_header())
        print("status org:", api_response.status_code)
        data = api_response.json()
        contenu_brut = api_response.text
        content_hash = hashlib.sha256(contenu_brut.encode('utf-8')).hexdigest()

        dico_entity = {}
        meta_donne = {}

        meta_donne["contenu_brut"] = contenu_brut
        meta_donne["status_code"] = api_response.status_code
        meta_donne["headers"] = json.dumps(dict(api_response.headers))
        meta_donne["contenu_hash"] = content_hash

        dico_entity["login"] = data.get("login")
        dico_entity["email"] = data.get("email")
        dico_entity["blog"] = data.get("blog")


        # Récupération de la liste des membres
        if dico_entity.get("members_url"):
            url_members_list = dico_entity["members_url"].replace("{/member}", "")
            api_response_members = requests.get(
                url_members_list, headers=self.get_request_header()
            )
            print("status members:", api_response_members.status_code)
            if api_response_members.status_code == 200:
                members_data = api_response_members.json()
                tableau_members = []
                for member in members_data:
                    tableau_members.append(member.get("login"))
                dico_entity["members_list"] = tableau_members

        return dico_entity, meta_donne
