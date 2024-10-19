from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app import app
from os import getenv

db = None
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

def db_commit(sql,parameters):
    """Handles commitable queries in database.
    Returns boolean whether commit was successful"""
    
    try:
        db.session.execute(sql, parameters)
        db.session.commit()
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


def db_execute(sql,parameters):
    """Handles SQL execute query in database. 
    Returns query_ok boolean and result of the query"""
    
    try:
        result = db.session.execute(sql, parameters)
        return True, result
    except IntegrityError as e:
        session.rollback()
        print(f"IntegrityError: {e}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"SQLAlchemyError: {e}")
    except Exception as e:
        session.rollback()
        print(f"Unexpected error: {e}")
    print("ERROR: db_execute")
    return False, None


class Food_stats(db.Model):
    """This class acts as mapping between database object and Python code"""

    foodid = db.Column(db.Integer, primary_key=True)
    foodname = db.Column(db.String)
    energia_laskennallinen = db.Column(db.Integer)
    rasva = db.Column(db.Integer)
    hiilihydraatti_imeytyva = db.Column(db.Integer)
    hiilihydraatti_erotuksena = db.Column(db.Integer)
    proteiini = db.Column(db.Integer)
    alkoholi = db.Column(db.Integer)
    tuhka = db.Column(db.Integer)
    vesi = db.Column(db.Integer)
    kcal = db.Column(db.Integer)

    def to_dict(self):
        return {
            "foodid": self.foodid,
            "foodname": self.foodname,
            "energia_laskennallinen": self.energia_laskennallinen,
            "rasva": self.rasva,
            "hiilihydraatti_imeytyva": self.hiilihydraatti_imeytyva,
            "hiilihydraatti_erotuksena": self.hiilihydraatti_erotuksena,
            "proteiini": self.proteiini,
            "alkoholi": self.alkoholi,
            "tuhka": self.tuhka,
            "vesi": self.vesi,
            "kcal": self.kcal,
        }

