import re
from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from db import Food_stats, db, Food
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db.init_app(app)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = text("SELECT id, password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()    
        if not user:
            return render_template("login.html", error_message="username_not_found")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = username
                return redirect("/")
            else:
                return render_template("login.html", error_message="wrong_password")        
        
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = text("SELECT id FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if user:
            return render_template("register.html", error=True, error_message="User already exists")
        if (len(password) < 4 or len(password)>30):
            return render_template("register.html", error=True, error_message="Password too long")
        else:
            hash_value = generate_password_hash(password)
            sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(sql, {"username":username,"password":hash_value})
            db.session.commit()
        #TODO: add check of username and password
        session["username"] = username
    return render_template("register.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/foodpage/<int:id>")
def foodpage(id):
    sql = text("""SELECT foodname
               ,ROUND(energia_laskennallinen,1)      as energia_laskennallinen
               ,ROUND(rasva,1)                       as rasva
               ,ROUND(hiilihydraatti_imeytyva,1)     as hiilihydraatti_imeytyva
               ,ROUND(hiilihydraatti_erotuksena,1)   as hiilihydraatti_erotuksena
               ,ROUND(proteiini,1)                   as proteiini
               ,ROUND(alkoholi,1)                    as alkoholi
               ,ROUND(tuhka,1)                       as tuhka
               ,ROUND(vesi,1)                        as vesi
               ,ROUND(kcal,1)                        as kcal
               FROM food_stats 
               WHERE foodid = (:id)""")
    result = db.session.execute(sql,{"id":id})
    food = result.fetchone()
    return render_template("foodpage.html", food_stats=food)

#@app.route("/my_page")
#def my_page():
#    #TODO: list of favourite foods and recipes

@app.route("/api/data")
def data():
    query = Food_stats.query

    # search filter:

    # below row parses the URL parameters (returns the part after question mark).
    # in this case it returns the value after ?search=
    search = request.args.get('search') 
    if search:
        query = query.filter(db.or_(
            Food_stats.foodname.ilike(f'%{search}%')
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in ['foodname']:
                name = 'foodname'
            col = getattr(Food_stats, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [food_stats.to_dict() for food_stats in query],
        'total': total,
    }

if __name__ == '__main__':
    app.run(debug=True)