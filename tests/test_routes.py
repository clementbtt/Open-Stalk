def test_index_without_auth(client):
    '''
    Test de l'endpoint / sans authetification client
    '''
    response = client.get("/")
    assert response.status_code == 302 # statut 302 : redirection puisque l'on n'est pas connecté

def test_index_with_auth(client):
    '''
    Test de l'endpoint / avec authentification client
    '''
    with client.session_transaction() as session: 
        session["authenticated"] = True # simulation d'une authentification
    response = client.get("/")
    assert response.status_code == 200 # nous voila connecté donc reponse 200



def test_login_page_display(client):
    '''
    Test de l'affichage de la page de connexion (GET)
    '''
    response = client.get("/user/login")
    assert response.status_code == 200 # nous voila connecté donc reponse 200
    assert b"login" in response.data or b"Connexion" in response.data # vérifie que le template login.html est bien rendu

def test_login_failure(client):
    '''
    Test de la connexion avec de mauvais identifiants
    '''
    payload = {"username": "Aïcha", "password": "bad_psswrd"} # fausses données
    response = client.post("/user/login", data=payload, follow_redirects=True)
    
    assert response.status_code == 200 # on est redirigé vers la page de login, qui s'affiche (200)
    assert b"Echec" in response.data # vérifie qu'un messsage d'erreur s'affiche

def test_register_page_display(client):
    '''
    Test de l'affichage de la page d'inscription (GET)
    '''
    response = client.get("/user/register")
    assert response.status_code == 200 # nous voila connecté donc reponse 200

def test_register_mismatch_password(client):
    '''
    Test d'échec d'inscription (mots de passe différents)
    '''
    payload = {
        "username": "toto", 
        "password": "1234", 
        "confirm_password": "567" # on entre un mot de passe différent
    }
    response = client.post("/user/register", data=payload, follow_redirects=True)
    
    assert response.status_code == 200 # la page se recharge
    assert b"correspondent pas" in response.data # on vérifie le message d'erreur "Les deux mots de passes ne correspondent pas !" s'affiche bien 

def test_logout(client):
    '''
    Test de la déconnexion et du nettoyage de session
    '''
   
    with client.session_transaction() as session: # On simule d'abord une session active
        session["authenticated"] = True # simulation d'une authentification
        session["username"] = "test"

   
    response = client.get("/user/logout", follow_redirects=True) 
    
    assert response.status_code == 302 or response.status_code == 200
    

    with client.session_transaction() as session:
        assert session.get("authenticated") is None # onvérifie que la clé n'existe plus, ou qu'elle n'est pas présente 

