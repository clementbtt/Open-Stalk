import hashlib
import json
import re
from injector import inject
from model.dao.IScrappingDAO import IScrappingDAO
from model.Artifact import Artifact
from model.Entity import Entity
from model.Relation import Relation

class FileScrappingManager:
    @inject
    def __init__(self, scrappingDAO: IScrappingDAO):
        self.__scrappingDAO = scrappingDAO

    def process(self, file_storage, source_id: int):
        """
        Traite un fichier uploadé (FileStorage de Flask)
        """
        filename = file_storage.filename
        content = file_storage.read().decode('utf-8', errors='ignore')
        
        # Calcul du hash (SHA-256)
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()

        # Création de l'artéfact
        artifact = Artifact()
        artifact.set_source_id(source_id)
        artifact.set_url(f"file://{filename}")
        artifact.set_content(content)
        artifact.set_contenu_hash(content_hash)
        artifact.set_status_code(200)
        artifact.set_headers(json.dumps({"filename": filename}))
        
        art_id = self.__scrappingDAO.add_artifact(artifact)

        # Logique d'extraction identique à WebScrappingManager
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        
        emails = list(set(re.findall(email_pattern, content)))
        ips = re.findall(ip_pattern, content)

        # Traitement des emails
        for email in emails:
            self._save_entity(email, 1, art_id, f"Trouvé dans le fichier {filename}")
        
        # Traitement des IPs (avec vérification 0-255)
        for ip in set(ips):
            parts = ip.split('.')
            if all(0 <= int(p) <= 255 for p in parts if p.isdigit()):
                self._save_entity(ip, 6, art_id, f"IP détectée dans le fichier {filename}")

    def _save_entity(self, value, type_id, art_id, context):
        entity = Entity()
        entity.set_element(value)
        entity.set_type_osint(type_id)
        ent_id = self.__scrappingDAO.add_entity(entity)
        
        relation = Relation()
        relation.set_artifact_id(art_id)
        relation.set_entity_id(ent_id)
        relation.set_context(context)
        self.__scrappingDAO.add_relation(relation)