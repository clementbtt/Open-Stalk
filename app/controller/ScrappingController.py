from flask import Flask, request, redirect, url_for, session, Response
from injector import inject
from model.managers.WikiScrappingManager import WikiScrappingManager
from model.managers.GithubScrappingManager import GithubScrappingManager
from model.Campaign import Campaign
from model.dao.ICampaignDAO import ICampaignDAO
from model.managers.WebScrappingManager import WebScrappingManager
from model.managers.SessionManager import SessionManager
from model.managers.FileScrappingManager import FileScrappingManager


class ScrappingController:
    """
    Controller des opérations de scrapping
    """

    @inject
    def __init__(
        self,
        wiki_scrapping_manager: WikiScrappingManager,
        github_scrapping_manager: GithubScrappingManager,
        web_scrapping_manager: WebScrappingManager,
        file_scrapping_manager: FileScrappingManager,
        campaign_dao: ICampaignDAO
    ):
        self.__wiki_scrapping_manager = wiki_scrapping_manager
        self.__github_scrapping_manager = github_scrapping_manager
        self.__web_scrapping_manager = web_scrapping_manager
        self.__file_scrapping_manager = file_scrapping_manager
        self.__campaign_dao = campaign_dao
        self.__session_manager = SessionManager()

    def run(self) -> Response:
        """
        Lance la procédure de scrapping 
        
        :param self: Description
        :return: Redirection vers la page de rendu
        :rtype: Response
        """
        campaign_id = request.form.get("campaign_id")
        campaign_id = int(campaign_id)
        campaign_data = self.__campaign_dao.get_campaign_by_id(campaign_id)
        campaign_name = campaign_data[1]

        subjects = request.form.getlist("subjects[]")
        urls = request.form.getlist("custom_urls[]")
        files = request.files.getlist("files[]")

        filenames = [f.filename for f in files if f.filename != '']
        active_subjects = [s for s in subjects if s.strip()]
        active_urls = [u for u in urls if u.strip()]
        
        details = f"Sujets: {', '.join(active_subjects)} | URLs: {', '.join(active_urls)} | Fichiers: {', '.join(filenames)}"

        self.__campaign_dao.add_audit_log(
            session.get("id"), 
            session.get("username"), 
            "SCRAPPING_RUN", 
            campaign_name, 
            details
        )

        for subject in subjects:
            if not subject.strip():
                continue

            subject_id = self.__campaign_dao.add_subject(subject, campaign_id)

            
            if request.form.get("use_git") == "yes": # Github est sélectionné
                source_id = self.__campaign_dao.add_source(
                    1, "api.github.com", campaign_id, subject_id
                )
                self.__github_scrapping_manager.process(subject, source_id)

            if request.form.get("use_wiki") == "yes": # Wikipédia est sélectionné
                source_id = self.__campaign_dao.add_source(
                    2, "api.wikimedia.org", campaign_id, subject_id
                )
                self.__wiki_scrapping_manager.process(subject, source_id)

        
        # Run sur les urls
        for url in urls:
            if url.strip():
                # Type source 4 correspond à "url personnalisé" dans le SQL
                source_id = self.__campaign_dao.add_source(3, url, campaign_id)
                self.__web_scrapping_manager.process(url, source_id)

        # Run sur les fichiers importé
        for file in files:
            if file:
                # Type source 4 correspond à "Fichier importé" dans le SQL
                source_id = self.__campaign_dao.add_source(4, file.filename, campaign_id)
                self.__file_scrapping_manager.process(file, source_id)

        return redirect(url_for('campaign.view_report', id=campaign_id))

    def register_routes(self, app: Flask):
        """
        Enregistre les routes du scrapping dans l'application

        :param app: Application dans laquelle on veut enregistrer les routes
        :type app: Flask
        """
        app.add_url_rule(
            rule="/scrapping/run",
            view_func=self.__session_manager.protect_endpoint(self.run),
            methods=["POST"],
            endpoint="scrapping.run",
        )
