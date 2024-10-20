from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db_commit, db_execute


def login(username, password):
    sql = text("SELECT id, username, password FROM users WHERE username=:username")
    query_ok, result = db_execute(sql, {"username": username})
    if query_ok:
        user = result.fetchone()
    else:
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
    """Used when checking new user registration.
    Returns False if username does not exist"""

    sql = text("""SELECT 1 FROM users WHERE users.username = :username""")
    query_ok, result = db_execute(sql, {"username": username})
    if query_ok and result.fetchone() is None:
        return False  # username does not exist
    else:
        return True  # username exists
