from model.dao.IScrappingDAO import IScrappingDAO
from model.Artifact import Artifact
from model.Entity import Entity
from model.Relation import Relation
from injector import inject
import requests
import hashlib
import json


class WikiScrappingManager:
    """
    Manager des opérations de scrapping wikipédia
    """

    @inject
    def __init__(self, scrappingDAO: IScrappingDAO):
        self.__scrappingDAO = scrappingDAO

    def process(self, input_value: str, source_id):
        '''
        Fonction qui prend en paramètre le cursor de la connection à la db et la value à rechercher.
        La fonction enregistre en base de donnée les informations de scraping lié à Wikipédia
        '''
        data_wiki, meta_donne = self.scraping_wikipedia(input_value)
        if data_wiki is None or meta_donne is None:
            return
        
        if data_wiki:
            artifact = Artifact()
            artifact.set_source_id(source_id)
            artifact.set_url(f"https://en.wikipedia.org/wiki/{data_wiki['titre'].replace(' ', '_')}")
            artifact.set_content(data_wiki['contenu'])
            artifact.set_contenu_hash(meta_donne["contenu_hash"])
            artifact.set_status_code(meta_donne["status_code"])
            artifact.set_headers(meta_donne["headers"])
            id = self.__scrappingDAO.add_artifact(artifact)
            artifact.set_id(id)

            if data_wiki.get('qid'):
                socials = self.scraping_wikidata(data_wiki['qid'])
                if socials:
                    data_entites = self.__scrappingDAO.get_data_types()
                    for type in data_entites:
                        id = type[0]
                        key = type[1]
                        element = socials.get(key)
                        if element:
                            entity = Entity()
                            entity.set_element(str(element))
                            entity.set_type_osint(id)
                            id = self.__scrappingDAO.add_entity(entity)
                            entity.set_id(id)

                            relation = Relation()
                            relation.set_artifact_id(artifact.get_id())
                            relation.set_entity_id(entity.get_id())
                            relation.set_context(f"{key} trouvé via Wikidata")
                            self.__scrappingDAO.add_relation(relation)
                        
    def scraping_wikipedia(self, subject: str):
        '''
        Fonction qui en fonction d'un sujet de recherche renvoie la page wikipédia.
        La fonction renvoie aussi l'identifiant qui va nous permettre d'aller chercher dans wikidata
        '''
        session = requests.Session()
        endpoint = "https://en.wikipedia.org/w/api.php"
        headers = {'User-Agent': 'MonApplicationOSINT/1.0 (adhoc4622@gmail.com)'}

        parametres = {
            "action": "query", 
            "list": "search", 
            "srsearch": subject, 
            "format": "json"
        }

        try:
            response = session.get(url=endpoint, params=parametres, headers=headers)
            contenu_brut = response.text
            data = response.json()
            resultats = data.get('query', {}).get('search', [])
            if not resultats: 
                return None, None
            titre_cible = resultats[0].get('title')
        except:
            return None, None


        params = {
            "action": "query", 
            "prop": "revisions|pageprops",
            "rvprop": "content", 
            "rvslots": "main",
            "titles": titre_cible,
            "format": "json",
            "formatversion": "2"
        }

        try:
            
            reponse_contenu = session.get(url=endpoint, params=params, headers=headers)
            contenu_brut = reponse_contenu.text
            meta_donne = {}
            meta_donne["contenu_brut"] = contenu_brut
            meta_donne["status_code"] = reponse_contenu.status_code
            meta_donne["headers"] = json.dumps(dict(reponse_contenu.headers))
            

            donnees_contenu = reponse_contenu.json()

            
            page = donnees_contenu['query']['pages'][0]
            contenu_hash = hashlib.sha256(contenu_brut.encode('utf-8')).hexdigest()
            meta_donne["contenu_hash"] = contenu_hash
            page_id = page.get('pageid')
            contenu_wiki = page['revisions'][0]['slots']['main']['content']
            qid = page.get('pageprops', {}).get('wikibase_item')
            return {
                "titre": titre_cible,
                "contenu": contenu_wiki,
                "pageid": page_id,
                "qid" : qid
            }, meta_donne
        except Exception as e:
            print(f"Erreur extraction : {e}")
            return None, None
        
    def scraping_wikidata(self, qid):
        '''
        Fonction qui en fonction d'un qid trouvé dans scrapping_wikipedia renvoie le insta, le twitter, le website et le facebook s'ils y sont.
        '''
        url = "https://www.wikidata.org/w/api.php"
        headers = {'User-Agent': 'MonApplicationOSINT/1.0 (raphael.loric@telecomnancy.net)'}
        params = {
            "action": "wbgetentities",
            "ids": qid,
            "format": "json",
            "props": "claims"
        }
        
        res = requests.get(url, params=params, headers=headers).json()
        data_requete = res['entities'][qid]['claims']
        
        results = {}
        
        dico = {
            'P2002': 'twitter',
            'P2003': 'instagram',
            'P856': 'website',
            'P2017' : 'facebook'
        }
        
        for prop_id, label in dico.items():
            if prop_id in data_requete:
                val = data_requete[prop_id][0]['mainsnak']['datavalue']['value']
                results[label] = val
                
        return results