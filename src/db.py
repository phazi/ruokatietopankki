from flask_sqlalchemy import SQLAlchemy
from app import app
from os import getenv

db = None
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


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
