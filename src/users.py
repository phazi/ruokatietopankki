from db import db, db_commit, db_execute
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session


def get_userid(username):
    sql = text("""SELECT id FROM users WHERE users.username = :username""")
    result = db.session.execute(sql, {"username": username})
    userid = result.fetchone()[0]
    return userid


def login(username, password):
    sql = text("SELECT id, username, password FROM users WHERE username=:username")
    query_ok, result = db_execute(sql, {"username": username})
    if query_ok:
        user = result.fetchone()
        print("def Login user query ok")
    else:
        print("ERROR: def Login user query")
        return False
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"] = user.username
            session["userid"] = user.id
            return True
        else:
            return False


def register(username, password):
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")

    if db_commit(sql, {"username": username, "password": hash_value}):
        login(username, password)
        return True
    else:
        return False


def username_exist(username):
    sql = text("""SELECT username FROM users WHERE users.username = :username""")
    query_ok, result = db_execute(sql, {"username": username})
    if query_ok and result.fetchone() is not None:
        return False
    else:
        return True

