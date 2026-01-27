from flask import Flask, render_template, request, redirect, url_for, session
from injector import Injector
from config.AppModule import AppModule
from controller.UserController import UserController
from controller.CampaignController import CampaignController
from controller.ScrappingController import ScrappingController
from model.managers.CampaignManager import CampaignManager
from model.managers.SessionManager import SessionManager
import os
from datetime import timedelta



# Création de la classe injector que s'occupera de l'injection de dépendance
injector = Injector([AppModule()])


# Création de l'application
app = Flask(__name__, template_folder="view", static_folder='view/static')

app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

campaign_manager = injector.get(CampaignManager)
session_manager = SessionManager()

# Création du UserController et enregistrement des routes dans l'application
user_controller = injector.get(UserController)
user_controller.register_routes(app)

campaign_controller = injector.get(CampaignController)
campaign_controller.register_routes(app)

scrapping_controller = injector.get(ScrappingController)
scrapping_controller.register_routes(app)

@app.route("/")
@session_manager.protect_endpoint
def dashboard():
    '''
    Affiche la page d'index
    '''
    user_id = session.get("id")
    # Récupération des campagnes de l'utilisateur
    data = campaign_controller.get_dashboard_statistics(user_id)
    
    return render_template(
        "dashboard.html", 
        campaigns=data["last_campaigns"], 
        stats=data["stats"]
    )



if __name__ == "__main__":
    app.run()