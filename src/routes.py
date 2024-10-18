import re
from flask import redirect, render_template, request, session, url_for
from sqlalchemy.sql import text
from db import Food_stats, db
import food
import users
import recipes
from app import app


@app.route("/")
def index():
    if "username" in session:
        userid = users.get_userid(session["username"])
        return render_template(
            "index.html",
            fav_food_rows=food.my_fav_foods(userid),
            my_recipe_rows=recipes.my_recipes_summary(userid),
        )
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error_message = 1
        if not (username and password):
            error_message = "Required fields are missing"
            return render_template("login.html", error_message=error_message)
        elif not users.login(username, password):
            error_message = "Wrong username or password"
            return render_template("login.html", error_message=error_message)
        else:
            return redirect("/")
    elif request.method == "GET":
        return render_template("/login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error_message = None
        if users.username_exist(username):
            error_message = "User already exists"
        elif len(password) < 4 or len(password) > 30:
            error_message = "Password must be 4-30 characters long"

        elif len(username) < 4 or len(username) > 30:
            error_message = "Username must be 4-30 characters long"

        elif not re.match(r"^[a-zA-Z0-9_\-.]+$", password):
            error_message = (
                "Password can contain only letters, numbers, and following symbols _-."
            )

        elif not re.match(r"^[a-zA-Z0-9]+$", username):
            error_message = "Username can contain only letters and numbers"

        elif not users.register(username, password):
            error_message = "An unexpected error happened"

        if error_message:
            return render_template(
                "register.html", error=True, error_message=error_message
            )
        else:
            return redirect("/")
    elif request.method == "GET":
        return render_template("register.html")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/foodpage/<int:id>")
def foodpage(id):
    food_sql = text("""SELECT foodid
               ,foodname
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
    food_result = db.session.execute(food_sql, {"id": id})
    food_row = food_result.fetchone()
    if "username" in session:
        if food.food_in_fav_foods(id, users.get_userid(session["username"])) is not None:
            return render_template(
                "foodpage.html", food_stats=food_row, fav_food_added=True
            )
        else:
            return render_template(
                "foodpage.html", food_stats=food_row, fav_food_added=False
            )
    else:
        return render_template("foodpage.html", food_stats=food_row)


@app.route("/foodpage/<int:id>/add_fav_food", methods=["POST"])
def add_fav_food(id):
    userid = users.get_userid(session["username"])
    if food.food_in_fav_foods(id, userid) is None:
        food.add_fav_foood(id, userid)
        foodpage_url = url_for("foodpage", id=id)
        print("add_fav_food iffissa")
        return redirect(foodpage_url)
    else:
        foodpage_url = url_for("foodpage", id=id)
        print("add_fav_food elsessa")
        return redirect(foodpage_url)


@app.route("/recipepage/<int:recipeid>")
def recipepage(recipeid):
    userid = users.get_userid(session["username"])
    recipe_sql = text("""SELECT recipe_foods.recipeid
                            ,user_recipes.name
                            ,user_recipes.description
                            ,user_recipes.created_ts
                            ,ROUND(SUM(food_stats.energia_laskennallinen * recipe_foods.amount), 1) AS energia_laskennallinen
                            ,ROUND(SUM(food_stats.rasva * recipe_foods.amount), 1) AS rasva
                            ,ROUND(SUM(food_stats.hiilihydraatti_imeytyva * recipe_foods.amount), 1) AS hiilihydraatti_imeytyva
                            ,ROUND(SUM(food_stats.hiilihydraatti_erotuksena * recipe_foods.amount), 1) AS hiilihydraatti_erotuksena
                            ,ROUND(SUM(food_stats.proteiini * recipe_foods.amount), 1) AS proteiini
                            ,ROUND(SUM(food_stats.alkoholi * recipe_foods.amount), 1) AS alkoholi
                            ,ROUND(SUM(food_stats.tuhka * recipe_foods.amount), 1) AS tuhka
                            ,ROUND(SUM(food_stats.vesi * recipe_foods.amount), 1) AS vesi
                            ,ROUND(SUM(food_stats.kcal * recipe_foods.amount), 1) AS kcal
                        FROM user_recipes
                        INNER JOIN recipe_foods ON user_recipes.userid = :userid
                            AND user_recipes.recipeid = :recipeid
                            AND user_recipes.recipeid = recipe_foods.recipeid
                        INNER JOIN food_stats ON recipe_foods.recipeid = user_recipes.recipeid
                            AND recipe_foods.foodid = food_stats.foodid
                        WHERE user_recipes.active = TRUE
                        GROUP BY recipe_foods.recipeid
                            ,user_recipes.name
                            ,user_recipes.description
                            ,user_recipes.created_ts""")
    recipe_result = db.session.execute(
        recipe_sql, {"userid": userid, "recipeid": recipeid}
    )
    recipe_first_row = recipe_result.fetchone()
    if recipe_first_row is None:
        return redirect("/")
    recipe_foods_sql = text("""SELECT recipe_foods.amount
                                ,food_stats.foodid
                                ,food_stats.foodname
                                ,ROUND(food_stats.energia_laskennallinen, 1) * recipe_foods.amount AS energia_laskennallinen
                                ,ROUND(food_stats.rasva, 1) * recipe_foods.amount AS rasva
                                ,ROUND(food_stats.hiilihydraatti_imeytyva, 1) * recipe_foods.amount AS hiilihydraatti_imeytyva
                                ,ROUND(food_stats.hiilihydraatti_erotuksena, 1) * recipe_foods.amount AS hiilihydraatti_erotuksena
                                ,ROUND(food_stats.proteiini, 1) * recipe_foods.amount AS proteiini
                                ,ROUND(food_stats.alkoholi, 1) * recipe_foods.amount AS alkoholi
                                ,ROUND(food_stats.tuhka, 1) * recipe_foods.amount AS tuhka
                                ,ROUND(food_stats.vesi, 1) * recipe_foods.amount AS vesi
                                ,ROUND(food_stats.kcal, 1) * recipe_foods.amount AS kcal
                            FROM recipe_foods
                            INNER JOIN food_stats ON recipe_foods.recipeid = :recipeid
                                AND recipe_foods.foodid = food_stats.foodid""")
    recipe_foods_results = db.session.execute(
        recipe_foods_sql, {"recipeid": recipe_first_row.recipeid}
    )
    recipe_food_rows = recipe_foods_results.fetchall()

    return render_template(
        "/recipepage.html",
        recipe_rows=recipe_food_rows,
        recipe_first_row=recipe_first_row,
    )


@app.route("/delete_recipe/<int:recipeid>")
def delete_recipe(recipeid):
    if "username" in session:
        userid = users.get_userid(session["username"])
    else:
        return redirect("/")
    del_recipe_sql = text("""UPDATE user_recipes SET active=FALSE
                        WHERE userid = :userid AND recipeid = :recipeid""")
    db.session.execute(del_recipe_sql, {"userid": userid, "recipeid": recipeid})
    db.session.commit()
    return redirect("/")


@app.route("/delete_fav_food/<int:foodid>")
def delete_fav_food(foodid):
    if "username" in session:
        userid = users.get_userid(session["username"])
    else:
        return redirect("/")
    del_fav_food_sql = text("""UPDATE user_fav_foods SET active=FALSE
                        WHERE userid = :userid AND foodid = :foodid""")
    db.session.execute(del_fav_food_sql, {"userid": userid, "foodid": foodid})
    db.session.commit()
    return redirect("/")


@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    if request.method == "POST":
        userid = users.get_userid(session["username"])
        description = request.form["description"]
        recipe_name = request.form["new_recipe"]
        foodid_list = request.form.getlist("foodid[]")
        amount_list = request.form.getlist("amount[]")

        insert_user_recipe_sql = text("""INSERT INTO user_recipes (userid,name,description,created_ts)
                             VALUES (:userid,:recipe_name,:description,NOW()) RETURNING recipeid""")  # returns the ID serial of the created row.
        result = db.session.execute(
            insert_user_recipe_sql,
            {"userid": userid, "recipe_name": recipe_name, "description": description},
        )  # result is the newest id that was just created by the insert
        newest_recipeid = result.fetchone()[0]
        db.session.commit()

        for foodid, amount in zip(foodid_list, amount_list):
            insert_recipe_foods_sql = text("""INSERT INTO recipe_foods (recipeid,foodid,amount)
                                           VALUES (:newest_recipeid,:foodid,:amount)""")
            db.session.execute(
                insert_recipe_foods_sql,
                {
                    "newest_recipeid": newest_recipeid,
                    "foodid": foodid,
                    "amount": amount,
                },
            )
            db.session.commit()
    return render_template("create_recipe.html")


@app.route("/api/data")
def data():
    query = Food_stats.query

    # search filter:

    # below row parses the URL parameters (returns the part after question mark).
    # in this case it returns the value after ?search=
    search = request.args.get("search")
    if search:
        query = query.filter(db.or_(Food_stats.foodname.ilike(f"%{search}%")))
    total = query.count()

    # sorting
    sort = request.args.get("sort")
    if sort:
        order = []
        for s in sort.split(","):
            direction = s[0]
            name = s[1:]
            if name not in ["foodname"]:
                name = "foodname"
            col = getattr(Food_stats, name)
            if direction == "-":
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    # pagination
    start = request.args.get("start", type=int, default=-1)
    length = request.args.get("length", type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        "data": [food_stats.to_dict() for food_stats in query],
        "total": total,
    }
