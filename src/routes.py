import re
from flask import redirect, render_template, request, session, url_for
from sqlalchemy.sql import text
from db import Food_stats, db, db_commit
import food
import users
import recipes
from app import app


@app.route("/")
def index():
    if "username" in session:
        userid = session["userid"]
        return render_template(
            "index.html",
            fav_food_rows=food.my_fav_foods(userid),
            my_recipe_rows=recipes.my_recipes_summary(userid),
        )
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("/login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error_message = None
        if not (username and password):
            error_message = "Required fields are missing"
            return render_template("login.html", error_message=error_message)
        elif not users.login(username, password):
            error_message = "Wrong username or password"
            return render_template("login.html", error_message=error_message)
        else:
            return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # username and password validity check:
        error_message = None
        if users.username_exist(username):
            error_message = "User already exists"
        elif len(password) < 4 or len(password) > 30:
            error_message = "Password must be 4-30 characters long"

        elif len(username) < 4 or len(username) > 30:
            error_message = "Username must be 4-30 characters long"

        elif not re.match(r"^[a-zA-ZåäöÅÄÖ0-9_\-.]+$", password):
            error_message = (
                "Password can contain only letters, numbers, and following symbols _-."
            )

        elif not re.match(r"^[a-zA-ZåäöÅÄÖ0-9]+$", username):
            error_message = "Username can contain only letters and numbers"

        elif not users.register(username, password):
            error_message = "An unexpected error happened"

        if error_message:
            return render_template(
                "register.html", error=True, error_message=error_message
            )
        else:
            return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/foodpage/<int:foodid>")
def foodpage(foodid):
    query_ok, result = food.get_food_stats(foodid)
    if query_ok:
        food_row = result.fetchone()
    if "username" in session:
        if food.food_in_fav_foods(foodid, session["userid"]) is not None:
            return render_template(
                "foodpage.html", food_stats=food_row, fav_food_added=True
            )
        else:
            return render_template(
                "foodpage.html", food_stats=food_row, fav_food_added=False
            )
    else:
        return render_template("foodpage.html", food_stats=food_row)


@app.route("/foodpage/<int:foodid>/add_fav_food", methods=["POST", "GET"])
def add_fav_food(foodid):
    foodpage_url = url_for("foodpage", foodid=foodid)
    if "username" in session:
        userid = session["userid"]
        if food.food_in_fav_foods(foodid, userid) is None:
            food.add_fav_foood(foodid, userid)
            return redirect(foodpage_url)
        else:
            return redirect(foodpage_url)
    else:
        return redirect(foodpage_url)


@app.route("/recipepage/<int:recipeid>")
def recipepage(recipeid):
    if "username" in session:
        userid = session["userid"]
    else:
        return redirect("/")

    recipe_first_row = recipes.recipe_summary(userid, recipeid).fetchone()
    if recipe_first_row is None:
        return redirect("/")

    recipe_food_rows = recipes.recipe_foods(recipeid)

    return render_template(
        "/recipepage.html",
        recipe_rows=recipe_food_rows,
        recipe_first_row=recipe_first_row,
    )


@app.route("/delete_recipe/<int:recipeid>", methods=["POST", "GET"])
def delete_recipe(recipeid):
    if "username" in session:
        userid = session["userid"]
    else:
        return redirect("/")
    del_recipe_sql = text("""UPDATE user_recipes SET active=FALSE
                        WHERE userid = :userid AND recipeid = :recipeid""")
    db_commit(del_recipe_sql, {"userid": userid, "recipeid": recipeid})
    return redirect("/")


@app.route("/delete_fav_food/<int:foodid>", methods=["POST"])
def delete_fav_food(foodid):
    if "username" in session:
        userid = session["userid"]
    else:
        return redirect("/")
    del_fav_food_sql = text("""UPDATE user_fav_foods SET active=FALSE
                        WHERE userid = :userid AND foodid = :foodid""")
    db_commit(del_fav_food_sql, {"userid": userid, "foodid": foodid})
    return redirect("/")


@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    error_message = None
    if request.method == "POST" and "username" in session:
        userid = session["userid"]

        description = request.form["description"]
        recipe_name = request.form["new_recipe"]
        foodids = request.form.getlist("foodid[]")  # returns list of strings
        amounts = request.form.getlist("amount[]")  # returns list of strings

        foodid_list = [int(foodid) for foodid in foodids]  # convert to list of integers
        amount_list = [int(amount) for amount in amounts]  # convert to list of integers

        # validating user input:
        error_message = None
        if len(recipe_name) < 1 or len(recipe_name) > 100:
            error_message = "Recipe name should be 1-100 characters long"
            return render_template("create_recipe.html", error_message=error_message)
        elif len(description) > 2000:
            error_message = "Description should be less than 2000 characters long"
            return render_template("create_recipe.html", error_message=error_message)

        valid_foodids = []
        invalid_foodids = []

        for item in foodid_list:
            if item not in food.get_foodids():
                invalid_foodids.append(item)
            else:
                valid_foodids.append(item)
        if invalid_foodids:
            error_message = f"""The following fooids were not recognized: {invalid_foodids}. 
                            These were valid: {valid_foodids}"""
            return render_template("create_recipe.html", error_message=error_message)
        elif min(amount_list) < 1:
            error_message = "Amounts should be greater than 0"
            return render_template("create_recipe.html", error_message=error_message)

        newest_recipeid = recipes.create_recipe(userid, recipe_name, description)

        for foodid, amount in zip(foodid_list, amount_list):
            row_insert_ok = recipes.add_food_to_recipe(newest_recipeid, foodid, amount)

            if not row_insert_ok:
                error_message = """An error occured when inserting food to recipe.
                Please try again."""
                return render_template(
                    "create_recipe.html", error_message=error_message
                )
        return render_template("create_recipe.html", error_message=None)

    elif request.method == "GET":
        if "username" in session:
            userid = session["userid"]
            return render_template("create_recipe.html", error_message=None)
        else:
            error_message = "Not logged in"
            return render_template("create_recipe.html", error_message=error_message)


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
            if name not in ['foodid','foodname', 'energia_laskennallinen', 'rasva', 'hiilihydraatti_imeytyva', 'proteiini', 'kcal']:
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
