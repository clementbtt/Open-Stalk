import requests
import re
import hashlib
import time
import json
from injector import inject
from model.dao.IScrappingDAO import IScrappingDAO
from model.Artifact import Artifact
from model.Entity import Entity
from model.Relation import Relation
from urllib.robotparser import RobotFileParser
import tldextract

USER_AGENT = "ProjetDetudeOSINT-TN-CART"
rate_limit_delay = 1
max_pages = 20

class WebScrappingManager:
    """
    Manager gérant la collecte de données via URL (Web Scraping).
    """

    @inject
    def __init__(self, scrappingDAO: IScrappingDAO):
        self.__scrappingDAO = scrappingDAO

    def process(self, start_url: str, source_id: int):
        """
        Parcours les urls interne d'un site et appelle scrape_and_save a chaque fois
        """
        domain = self._normalize_domain(start_url)
        rp = RobotFileParser()
        rp.set_url(f"https://{domain}/robots.txt")
        try:
            rp.read()
        except:
            pass  # Si le robots.txt n'existe pas, on continue quand même

        to_visit = [start_url]
        visited = set()
        
        trash = [".jpg", ".png", ".css", ".js", ".ico", ".svg", ".pdf", ".zip"]

        while len(to_visit) > 0 and len(visited) < max_pages:
            current_url = self._canonicalize_url(to_visit.pop(0))
             
            # on vérifie si l'url est autorisée par le robots.txt et si on l'a pas déjà visitée
            # utilisation direct de la fonction is_valid_robots
            if rp.can_fetch(USER_AGENT, current_url) and current_url not in visited:
                
                # et la on vérifie si l'url comporte un des extensions à ignorer
                is_trash = False
                for ext in trash:
                    if ext in current_url.lower():
                        is_trash = True
                        break
                
                if not is_trash:
                    # Scraping de la page actuelle
                    page_content = self._scrape_and_save(current_url, source_id)
                    visited.add(current_url)

                    if page_content:
                        # ON RECHERCHE LES LIENS POUR LE CRAWLING ET EXPLORER DE NOUVELLES PAGES
                        links = re.findall(r'href=["\'](https?://[^\s"\']+|/[^\s"\']+)["\']', page_content)
                        for l in links:
                            full_link = ""
                            # cas où l'url est complet
                            if l.startswith("https") or l.startswith("http"):
                                full_link = l
                            # cas où l'url est relatif au domaine
                            elif l.startswith("/"):
                                full_link = f"https://{domain}{l}"
                            # cas où l'url est relative au dossier actuel
                            else:
                                if current_url.endswith("/"):
                                    base = current_url
                                else:
                                    base = current_url.rsplit('/', 1)[0] + "/"
                                full_link = base + l
                            
                            # On vérifie qu'on reste bien sur le domaine et qu'on n'a pas déjà visité
                            if self._normalize_domain(full_link) == domain and full_link not in visited:
                                to_visit.append(full_link)
                    
                    visited.add(current_url)

    def _scrape_and_save(self, url, source_id):
        """
        Fonction qui va scraper les infos d'une page (fusion de fetch_html et process_page)
        """
        try:
            time.sleep(1)
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(url, headers=headers, timeout=rate_limit_delay)
            
            if response.status_code != 200:
                return None

            content = response.text
            
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()

            artifact = Artifact()
            artifact.set_source_id(source_id)
            artifact.set_url(url)
            artifact.set_content(content) 
            artifact.set_contenu_hash(content_hash)
            artifact.set_status_code(response.status_code)
            artifact.set_headers(json.dumps(dict(response.headers)))
            
            art_id = self.__scrappingDAO.add_artifact(artifact)
            artifact.set_id(art_id)

            #formules regex pour les emails et les ips
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
            
            emails = list(set(re.findall(email_pattern, content)))
            ips = re.findall(ip_pattern, content)

            valid_ips = []
            for ip in ips:
                parts = ip.split('.')
                # on vérifie que les chiffres sont bien contenus entre 0 et 255
                if len(parts) == 4:
                    if all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
                        if parts[0]: # On vérifie qu'il y a bien un premier segment
                            valid_ips.append(ip)
            valid_ips = list(set(valid_ips))

            # Sauvegarde des emails 
            for email in emails:
                self._save_entity(email, 1, art_id, f"Trouvé sur {url}")
            
            # Sauvegarde des IPs 
            for ip in valid_ips:
                self._save_entity(ip, 6, art_id, f"IP détectée sur {url}")

            return content
        except Exception as e:
            print(f"Erreur sur {url}: {e}")
            return None

    def _save_entity(self, value, type_id, art_id, context):
        """Enregistre une entité et sa relation avec l'artéfact."""
        entity = Entity()
        entity.set_element(value)
        entity.set_type_osint(type_id)
        ent_id = self.__scrappingDAO.add_entity(entity)
        
        relation = Relation()
        relation.set_artifact_id(art_id)
        relation.set_entity_id(ent_id)
        relation.set_context(context)
        self.__scrappingDAO.add_relation(relation)

    def _canonicalize_url(self, url):
        """Permet de supprimer les / et les # d'une url"""
        url = url.split('#')[0]
        if len(url) > 1 and url[-1] == "/":
            url = url[:-1]
        return url
    
    def _normalize_domain(self, url):
        """Normalise le domaine d'une url pour ne renvoyer que le domaine principal."""
        ext = tldextract.extract(url)
        return f"{ext.domain}.{ext.suffix}"
