from flask import Flask, Response, render_template, request, redirect, url_for, session
from injector import inject
from model.managers.UserManager import UserManager
from model.managers.CampaignManager import CampaignManager
from model.managers.SessionManager import SessionManager


class UserController:
    """
    Controller de l'entité utilisateur
    """

    @inject
    def __init__(self, user_manager: UserManager, campaign_manager: CampaignManager):
        """
        Constructeur de la classe

        :param user_manager: Manager utilisateur foruni par injection de dépendances
        :type user_manager: UserManager
        """
        self.__user_manager = user_manager
        self.__campaign_manager = campaign_manager
        self.__session_manager = SessionManager()

    def check_authentication(self) -> Response:
        """
        Vérifie les informations de connexion saisie par l'utilisateur

        :return: Redirection vers la page d'index, si les informations sont correctes, vers la page de connexion sinon
        :rtype: Response
        """
        redirection = redirect(url_for("dashboard"))
        try:
            username = request.form["username"]
            password = request.form["password"]
            assert self.__user_manager.check_authentication(username, password)

            user_id = self.__user_manager.get_user_id_from_username(username)
            session["id"] = user_id
            session["username"] = username
            session["authenticated"] = True

            self.__campaign_manager.add_audit_log(
            user_id=user_id,
            username=username,
            action="LOGIN",
            campaign_name="/",
            target_details="Connexion réussie à la plateforme"
        )
            session.permanent = True
        except Exception as e:
            print(e)
            redirection = redirect(
                url_for("user.show_login", error="Echec de l'authentification !")
            )
        return redirection

    def show_login(self) -> str:
        """
        Affiche la page de connexion

        :return: La page de connexion
        :rtype: str
        """
        error = request.args.get("error", "")
        return render_template("login.html", error=error)

    def register(self) -> Response:
        """
        Initie la procédure d'inscription

        :return: Redirection vers la page de connexion si l'inscription à fonctionné, vers la page d'inscription sinon
        :rtype: Response
        """
        redirection = redirect(url_for("user.show_login"))
        try:
            username = request.form["username"]
            password = request.form["password"]
            confirmation = request.form["confirm_password"]
            if password == confirmation:
                self.__user_manager.register(username, password)
            else:
                error = "Les deux mots de passes ne correspondent pas !"
                redirection = redirect(url_for("user.show_register", error=error))
        except Exception as e:
            error = "Echec de l'inscription, veuillez réessayer ultérieurement !"
            print(e)
            redirection = redirect(url_for("user.show_register", error=error))
        return redirection

    def show_register(self) -> str:
        """
        Affiche la page d'inscription

        :return: La page d'inscription
        :rtype: str
        """
        error = request.args.get("error", "")
        return render_template("register.html", error=error)

    def logout(self) -> Response:
        self.__campaign_manager.add_audit_log(
            user_id=session.get("id"),
            username=session.get("username"),
            action="LOGOUT",
            campaign_name="/",
            target_details="Déconnexion de l'utilisateur"
        )
        session.clear()
        return redirect(url_for("dashboard"))

    def register_routes(self, app: Flask):
        """
        Enregistre les routes dans l'application

        :param app: Application dans laquelle on veut enregistrer les routes
        :type app: Flask
        """
        app.add_url_rule(
            rule="/user/login",
            view_func=self.check_authentication,
            methods=["POST"],
            endpoint="user.check_authentication",
        )
        app.add_url_rule(
            rule="/user/login",
            view_func=self.show_login,
            methods=["GET"],
            endpoint="user.show_login",
        ),
        app.add_url_rule(
            rule="/user/register",
            view_func=self.register,
            methods=["POST"],
            endpoint="user.register",
        ),
        app.add_url_rule(
            rule="/user/register",
            view_func=self.show_register,
            methods=["GET"],
            endpoint="user.show_register",
        ),
        app.add_url_rule(
            rule="/user/logout",
            view_func=self.__session_manager.protect_endpoint(self.logout),
            methods=["GET"],
            endpoint="user.logout",
        )
