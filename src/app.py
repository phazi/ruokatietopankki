from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///postgres"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return "Tervetuloa Ruokatietopankkiin!"

@app.route("/page/<int:id>")
def page(id):
    sql = text("SELECT foodname FROM food WHERE foodid = (:id)")
    result = db.session.execute(sql,{"id":id})
    food_name = result.fetchone()
    return "Tämä on sivu " + str(id) + " eli " + food_name.foodname

@app.route("/test")
def test():
    content = ""
    for i in range(100):
        content += str(i + 1) + " "
    return content