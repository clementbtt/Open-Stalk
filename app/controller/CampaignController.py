from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    Response,
    jsonify,
)
from injector import inject
from model.managers.CampaignManager import CampaignManager
from model.managers.SessionManager import SessionManager


class CampaignController:
    """
    Controller des campagnes
    """

    @inject
    def __init__(self, campaign_manager: CampaignManager):
        self.__campaign_manager = campaign_manager
        self.__session_manager = SessionManager()

    def show_campaign_settings(self, id: int) -> Response | str:
        """
        Affiche la page de paramétrage d'une campagne

        :param id: Id de la campagne à paramétrer
        :type id: int
        :return: Une redirection vers le dashboard si la campagne n'existe pas, sinon retourne la template de paramétrage de la campagne
        :rtype: Response | str
        """
        campaign = self.__campaign_manager.get_campaign_by_id(id)
        if not campaign:
            return redirect(url_for("dashboard"))

        # Récupération des sujets existants
        existing_subjects = self.__campaign_manager.get_campaign_subjects(id)

        return render_template(
            "campaign.html",
            campaign_id=id,
            campaign_name=campaign[1],
            subjects=existing_subjects, 
        )

    def create(self) -> Response:
        """
        Affiche la page de création d'une campagne

        :return: Redirection vers la page de dashboard
        :rtype: Response
        """
        title = request.form.get("title")
        user_id = session.get("id")
        username = session.get("username")

        self.__campaign_manager.create_new_campaign(title, user_id)

        self.__campaign_manager.add_audit_log(
            user_id=user_id,
            username=username,
            action="CREATE_CAMPAIGN",
            campaign_name=title,
            target_details=f"Création de la campagne par l'utilisateur {username}"
        )

        return redirect(url_for("dashboard"))

    def delete(self, id: int) -> Response:
        """
        Supprime une campagne

        :param id: Id de la campagne à supprimer
        :type id: int
        :return: Redirection vers la page de dashboard
        :rtype: Response
        """
        campaign_data = self.__campaign_manager.get_campaign_by_id(id)
        campaign_name = campaign_data[1]
        self.__campaign_manager.add_audit_log(
            user_id=session.get("id"),
            username=session.get("username"),
            action="DELETE_CAMPAIGN",
            campaign_name=campaign_name,
            target_details="Campagne supprimée par l'utilisateur"
        )
        user_id = session.get("id")
        if user_id:
            self.__campaign_manager.delete_campaign(id, user_id)
        return redirect(url_for("dashboard"))

    def get_user_campaigns(self, id: int) -> list:
        """
        Récupère les campagnes de l'utilisateur

        :param id: Id de l'utilisateur dont on veut récupérer les campagnes
        :type id: int
        :return: La liste des campagnes de l'utilisateur
        :rtype: list
        """
        return self.__campaign_manager.get_user_campaigns(id)
    
    def get_dashboard_statistics(self, user_id: int):
        """
        Récupère les données formatées pour le dashboard via le manager.
        """
        return self.__campaign_manager.get_dashboard_data(user_id)
    
    def list_all_campaigns(self):
        user_id = session.get("id")
        campaigns = self.__campaign_manager.get_user_campaigns(user_id) 
        return render_template("all_campaigns.html", campaigns=campaigns)

    def list_all_sources(self):
        user_id = session.get("id")
        sources = self.__campaign_manager.get_all_sources(user_id)
        return render_template("all_sources.html", sources=sources)

    def export(self, id: int) -> Response:
        data = self.__campaign_manager.export_campaign_json(id)

        self.__campaign_manager.add_audit_log(
            user_id=session.get("id"),
            username=session.get("username"),
            action="EXPORT_JSON",
            campaign_name=data["metadata"]["titre"],
            target_details=f"Export complet de {len(data['preuves'])} artefacts"
        )
        
        return jsonify(data)

    def view_report(self, id: int) -> str | Response:
        """
        Affiche le résultat d'une campagne

        :param id: Id de la campagne dont on veut afficher les résultats
        :type id: int
        :return: Une redirection vers la page dashboard si la campagne n'existe pas, sinon affiche la page de résultats
        :rtype: str | Response
        """
        campaign_data = self.__campaign_manager.export_campaign_json(id)

        if not campaign_data or not campaign_data.get("metadata"):
            return redirect(url_for("dashboard"))

        findings = campaign_data.get("preuves", [])

        api_results = []
        web_results = []

        api_keywords = ["github.com", "wikipedia.org", "wikimedia.org", "file://"]

        for f in findings:
            url_lower = f["url"].lower()
            est_une_api = False

            # On vérifie si l'URL contient l'un des mots-clés
            for k in api_keywords:
                if k in url_lower:
                    est_une_api = True
                    break

            if est_une_api:
                api_results.append(f)
            else:
                web_results.append(f)

        return render_template(
            "render_campaign.html",
            campaign_id=id,
            campaign_name=campaign_data["metadata"]["titre"],
            api_results=api_results,
            web_results=web_results,
            type_labels={
                1: "Email",
                2: "Pseudo",
                3: "Twitter",
                4: "Instagram",
                5: "Website",
                6: "IP",
                7: "Facebook",
            },
        )
    
    def show_rgpd(self):
        """Affiche la page d'information sur la politique RGPD."""
        return render_template("rgpd.html")

    def register_routes(self, app: Flask):
        """
        Enregistre les routes dans l'application

        :param app: Application dans laquelle on veut enregistrer les routes
        :type app: Flask
        """
        app.add_url_rule(
            rule="/campaign/create",
            view_func=self.__session_manager.protect_endpoint(self.create),
            methods=["POST"],
            endpoint="campaign.create",
        )
        app.add_url_rule(
            rule="/campaign/delete/<int:id>",
            view_func=self.__session_manager.protect_endpoint(self.delete),
            methods=["GET"],
            endpoint="campaign.delete",
        )
        app.add_url_rule(
            rule="/campaign/settings/<int:id>",
            view_func=self.__session_manager.protect_endpoint(
                self.show_campaign_settings
            ),
            methods=["GET"],
            endpoint="campaign.show_campaign_settings",
        )
        app.add_url_rule(
            rule="/campaign/export/<int:id>",
            view_func=self.__session_manager.protect_endpoint(self.export),
            methods=["GET"],
            endpoint="campaign.export",
        )
        app.add_url_rule(
            rule="/campaign/report/<int:id>",
            view_func=self.__session_manager.protect_endpoint(self.view_report),
            methods=["GET"],
            endpoint="campaign.view_report",
        )
        app.add_url_rule(
            "/campaigns",
            view_func=self.__session_manager.protect_endpoint(self.list_all_campaigns), 
            endpoint="campaign.list_all")
        app.add_url_rule(
            "/sources", 
            view_func=self.__session_manager.protect_endpoint(self.list_all_sources),
            endpoint="campaign.list_sources"
            )
        app.add_url_rule(
            rule="/rgpd",
            view_func=self.__session_manager.protect_endpoint(self.show_rgpd),
            methods=["GET"],
            endpoint="campaign.show_rgpd"
            )
