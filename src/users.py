from db import db
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
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
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
    try:
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
        login(username, password)
        return True
    except IntegrityError as e:
        session.rollback()
        print(f"IntegrityError: {e}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"SQLAlchemyError: {e}")
    
    except Exception as e:
        session.rollback()
        print(f"Unexpected error: {e}")
    return False


def username_exist(username):
    sql = text("""SELECT username FROM users WHERE users.username = :username""")
    result = db.session.execute(sql, {"username": username})
    username = result.fetchone()
    if username is None:
        return False
    else:
        return True
