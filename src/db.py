from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

db = SQLAlchemy()

class Food(db.Model):
    """This class acts as mapping between database object and Python code"""

    foodid = db.Column(db.Integer, primary_key=True)
    edport = db.Column(db.Integer)
    foodtype = db.Column(db.String)
    process = db.Column(db.String)
    fuclassp = db.Column(db.String)
    igclass = db.Column(db.String)
    igclassp = db.Column(db.String)
    fuclass = db.Column(db.String)
    foodname = db.Column(db.String)

    def to_dict(self):
        return {
            'foodid': self.foodid,
            'edport': self.edport,
            'foodtype': self.foodtype,
            'process': self.process,
            'fuclassp': self.fuclassp,
            'igclass': self.igclass,
            'igclassp': self.igclassp,
            'fuclass': self.fuclass,
            'foodname': self.foodname
        }


class Food_stats(db.Model):
    """This class acts as mapping between database object and Python code"""

    foodid = db.Column(db.Integer, primary_key=True)
    foodname = db.Column(db.String)
    energia_laskennallinen = db.Column(db.Integer)
    rasva = db.Column(db.Integer)
    hiilihydraatti_imeytyvä = db.Column(db.Integer)
    hiilihydraatti_erotuksena = db.Column(db.Integer)
    proteiini = db.Column(db.Integer)
    alkoholi = db.Column(db.Integer)
    tuhka = db.Column(db.Integer)
    vesi = db.Column(db.Integer)

    def to_dict(self):
        return {
            'foodid': self.foodid,
            'foodname': self.foodname,
            'energia_laskennallinen': self.energia_laskennallinen,
            'rasva': self.rasva,
            'hiilihydraatti_imeytyvä': self.hiilihydraatti_imeytyvä,
            'hiilihydraatti_erotuksena': self.hiilihydraatti_erotuksena,
            'proteiini': self.proteiini,
            'alkoholi': self.alkoholi,
            'tuhka': self.tuhka,
            'vesi': self.vesi
        }