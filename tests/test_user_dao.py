from app.model.User import User
import bcrypt

def test_add_user(user_dao, database):
    assert get_length_of_table(database) == 0
    user = User()
    password = "password hashé"
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    user.set_username("toto")
    user.set_password(hashed_password)
    user_dao.register(user)
    assert get_length_of_table(database) == 1
    added_user = get_last_user_added(database)
    assert added_user[1] == "toto"
    assert bcrypt.checkpw(password_bytes, added_user[2])

def test_get_user_by_username(user_dao):
    user = User()
    user.set_username("tata")
    user.set_password("uedfhbdifvgfijbvfgtb")
    user_dao.register(user)
    user_by_username = user_dao.get_user_by_username("tata")
    assert user_by_username.get_password() == "uedfhbdifvgfijbvfgtb"

def test_check_authentication(user_dao):
    user = User()
    user.set_username("user1")
    password = "password"
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    user.set_password(hashed_password)
    user_dao.register(user)
    
    connection_attempt1 = User()
    connection_attempt1.set_username("wrong user")
    connection_attempt1.set_password("wrong password")
    assert user_dao.check_authentication(connection_attempt1) == False

    connection_attempt2 = User()
    connection_attempt2.set_username("user1")
    connection_attempt2.set_password("wrong password")
    assert user_dao.check_authentication(connection_attempt2) == False

    connection_attempt3 = User()
    connection_attempt3.set_username("wrong user")
    connection_attempt3.set_password("password")
    assert user_dao.check_authentication(connection_attempt3) == False

    connection_attempt4 = User()
    connection_attempt4.set_username("user1")
    connection_attempt4.set_password("password")
    assert user_dao.check_authentication(connection_attempt4) == True
    


def get_length_of_table(database):
    database.connect()
    legnth = database.execute_query("select count(*) from users;")
    database.disconnect()
    return legnth[0][0]

def get_last_user_added(database):
    database.connect()
    user = database.execute_query("select * from users order by user_id desc;")
    database.disconnect()
    return user[0]


    