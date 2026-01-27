from model.dao.ICampaignDAO import ICampaignDAO
from model.dao.IDatabase import IDatabase
from injector import inject
from flask import request

class CampaignDAO(ICampaignDAO):
    """
    Class pour gérer les campagnes
    """
    @inject
    def __init__(self, database: IDatabase):
        self.__database = database

    def create_campaign(self, title: str, user_id: int):
        self.__database.connect()
        params = (title, user_id)
        self.__database.execute_non_query("INSERT INTO campagnes (titre, owner_id) VALUES (?, ?)", params)
        self.__database.disconnect()

    def get_campaigns_by_user(self, user_id: int) -> list:
        self.__database.connect()
        query = "SELECT campagne_id, titre FROM campagnes WHERE owner_id = ?"
        data = self.__database.execute_query(query, (user_id,))
        self.__database.disconnect()
        return data 
    
    def delete_campaign(self, campaign_id: int, user_id: int):
        self.__database.connect()
        query = "DELETE FROM campagnes WHERE campagne_id = ? AND owner_id = ?"
        self.__database.execute_non_query(query, (campaign_id, user_id))
        query_entite_delete = "DELETE FROM entites WHERE entite_id NOT IN (SELECT DISTINCT entite_id FROM relations);"
        self.__database.execute_non_query(query_entite_delete)
        self.__database.disconnect()

    def add_subject(self, title: str, campaign_id: int) -> int:
        self.__database.connect()
        query_check = "SELECT sujet_id FROM sujets_recherche WHERE libelle = ? AND campagne_id = ?"
        existing = self.__database.execute_query(query_check, (title, campaign_id))
        if existing:
            subject_id = existing[0][0]
        else:
            self.__database.execute_non_query("INSERT INTO sujets_recherche (libelle, campagne_id) VALUES (?, ?)", (title, campaign_id))
            res = self.__database.execute_query("SELECT MAX(sujet_id) FROM sujets_recherche")
            subject_id = res[0][0]
        self.__database.disconnect()
        return subject_id

    def add_source(self, type_source: int, url: str, campagne_id: int, subject_id: int = None) -> int:
        self.__database.connect()
        check_query = ("SELECT source_id FROM sources WHERE type_source = ? AND url = ? AND campagne_id = ? AND (sujet_id = ? OR (sujet_id IS NULL AND ? IS NULL))")
        params_check = (type_source, url, campagne_id, subject_id, subject_id)
        existing = self.__database.execute_query(check_query, params_check)
        if existing:
            source_id = existing[0][0]
        else:
            params = (type_source, url, campagne_id, subject_id)
            self.__database.execute_non_query("INSERT INTO sources (type_source, url, campagne_id, sujet_id) VALUES (?, ?, ?, ?)", params)
            res = self.__database.execute_query("SELECT MAX(source_id) FROM sources")
            source_id = res[0][0]
        self.__database.disconnect()
        return source_id

    def get_campaign_by_id(self, campaign_id: int) -> tuple|None: 
        self.__database.connect()
        data = self.__database.execute_query("SELECT * FROM campagnes WHERE campagne_id = ?", (campaign_id,))
        self.__database.disconnect()
        return data[0] if data else None
    
    def get_subjects_by_campaign(self, campaign_id: int) -> list:
        self.__database.connect()
        query = "SELECT libelle FROM sujets_recherche WHERE campagne_id = ?"
        data = self.__database.execute_query(query, (campaign_id,))
        self.__database.disconnect()
        return [row[0] for row in data]
    
    def get_user_stats_detailed(self, user_id: int) -> dict:
        """Récupère le décompte détaillé des sources et entités par type."""
        self.__database.connect()
        
        query_sources = """
            SELECT ts.nom, COUNT(s.source_id)
            FROM sources s
            JOIN types_sources ts ON s.type_source = ts.type_source_id
            JOIN campagnes c ON s.campagne_id = c.campagne_id
            WHERE c.owner_id = ?
            GROUP BY ts.nom
        """
        
        query_entities = """
            SELECT te.nom, COUNT(DISTINCT e.entite_id)
            FROM entites e
            JOIN types_entites te ON e.type_osint_id = te.type_entite_id
            JOIN relations r ON e.entite_id = r.entite_id
            JOIN artefacts a ON r.artefact_id = a.artefact_id
            JOIN sources s ON a.source_id = s.source_id
            JOIN campagnes c ON s.campagne_id = c.campagne_id
            WHERE c.owner_id = ?
            GROUP BY te.nom
        """
        
        sources_raw = self.__database.execute_query(query_sources, (user_id,))
        entities_raw = self.__database.execute_query(query_entities, (user_id,))
        self.__database.disconnect()
        
        dict_sources = {}
        total_source = 0
        
        dict_entities = {}
        total_entite = 0

        for ligne in sources_raw:
            nom_type = ligne[0]   
            quantite = ligne[1]   
            
            dict_sources[nom_type] = quantite
            total_source = total_source + quantite

        for ligne in entities_raw:
            nom_entite = ligne[0] 
            quantite = ligne[1]  
            
            dict_entities[nom_entite] = quantite
            total_entite = total_entite + quantite

        return {
            "sources": dict_sources,
            "entities": dict_entities,
            "total_sources": total_source,
            "total_entities": total_entite
        }

    def get_all_user_sources(self, user_id: int) -> list:
        """Liste toutes les sources de l'utilisateur avec le nom de la campagne."""
        self.__database.connect()
        query = """
            SELECT s.url, ts.nom, c.titre, s.source_id
            FROM sources s
            JOIN campagnes c ON s.campagne_id = c.campagne_id
            JOIN types_sources ts ON s.type_source = ts.type_source_id
            WHERE c.owner_id = ?
        """
        data = self.__database.execute_query(query, (user_id,))
        self.__database.disconnect()
        return data
    
    def get_last_five_campaigns(self, user_id: int) -> list:
        """Récupère uniquement les 5 dernières campagnes créées."""
        self.__database.connect()
        query = """
            SELECT campagne_id, titre 
            FROM campagnes 
            WHERE owner_id = ? 
            ORDER BY date_creation DESC 
            LIMIT 5
        """
        data = self.__database.execute_query(query, (user_id,))
        self.__database.disconnect()
        return data
    
    def get_full_campaign_data(self, campaign_id: int) -> dict:
        self.__database.connect()
        
        campagne = self.__database.execute_query("SELECT * FROM campagnes WHERE campagne_id = ?", (campaign_id,))
        
        query = """
            SELECT 
                a.artefact_id, a.url, a.contenu_brut, a.contenu_hash, a.date_collecte,
                e.element, e.type_osint_id, r.contexte_extrait, e.entite_id
            FROM artefacts a
            JOIN sources s ON a.source_id = s.source_id
            LEFT JOIN relations r ON a.artefact_id = r.artefact_id
            LEFT JOIN entites e ON r.entite_id = e.entite_id
            WHERE s.campagne_id = ?
        """
        results = self.__database.execute_query(query, (campaign_id,))
        self.__database.disconnect()

        metadata = {"id": campagne[0][0], "titre": campagne[0][1], "date": campagne[0][2]} if campagne else {}
        
        preuves = {}
        findings = {}

        for row in results:
            art_id, url, brut, sha, date, element, type_id, contexte, ent_id = row
            if art_id not in preuves:
                preuves[art_id] = {
                    "url": url,
                    "hash": sha,
                    "contenu_brut": brut,
                    "date": date,
                    "entites": []
                }
            
            if element:
                preuves[art_id]["entites"].append({"valeur": element, "contexte": contexte})
                
                if ent_id not in findings:
                    findings[ent_id] = {"valeur": element, "type": type_id, "occurrences": 1}
                else:
                    findings[ent_id]["occurrences"] += 1

        return {
            "metadata": metadata,
            "findings": list(findings.values()),
            "preuves": list(preuves.values())
        }
    
    def add_audit_log(self, user_id, username, action, campaign_name, target_details):
        self.__database.connect()
        
        ip = request.remote_addr if request else "127.0.0.1"
        
        query = """INSERT INTO audit_logs (user_id, username, action, campaign_name, target_details, ip_address) 
                VALUES (?, ?, ?, ?, ?, ?)"""
        params = (user_id, username, action, campaign_name, target_details, ip)
        self.__database.execute_non_query(query, params)
        self.__database.disconnect()