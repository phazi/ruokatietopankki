from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app import app
from os import getenv

db = None
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


def db_commit(sql, parameters):
    """Handles commitable queries in database.
    Returns boolean whether commit was successful"""

    try:
        db.session.execute(sql, parameters)
        db.session.commit()
        return True
    except IntegrityError as e:
        db.session.rollback()
        print(f"IntegrityError: {e}")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"SQLAlchemyError: {e}")
    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {e}")
    return False


def db_execute(sql, parameters):
    """Handles SQL execute query in database.
    Returns query_ok boolean and result of the query"""

    try:
        result = db.session.execute(sql, parameters)
        return True, result
    except IntegrityError as e:
        db.session.rollback()
        print(f"IntegrityError: {e}")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"SQLAlchemyError: {e}")
    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {e}")
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
            "energia_laskennallinen": round(float(self.energia_laskennallinen),1),
            "rasva": round(float(self.rasva),1),
            "hiilihydraatti_imeytyva": round(float(self.hiilihydraatti_imeytyva),1),
            "hiilihydraatti_erotuksena": round(float(self.hiilihydraatti_erotuksena),1),
            "proteiini": round(float(self.proteiini),1),
            "alkoholi": round(float(self.alkoholi),1),
            "tuhka": round(float(self.tuhka),1),
            "vesi": round(float(self.vesi),1),
            "kcal": round(float(self.kcal),1),
        }
