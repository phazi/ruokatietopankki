from db import db, db_commit, db_execute
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def my_recipes_summary(userid):
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
                            AND user_recipes.recipeid = recipe_foods.recipeid
                        INNER JOIN food_stats ON recipe_foods.recipeid = user_recipes.recipeid
                            AND recipe_foods.foodid = food_stats.foodid
                        WHERE user_recipes.active = TRUE
                        GROUP BY recipe_foods.recipeid
                            ,user_recipes.name
                            ,user_recipes.description
                            ,user_recipes.created_ts""")
    query_ok, recipe_result = db_execute(recipe_sql, {"userid": userid})
    if query_ok:
        return recipe_result.fetchall()
    else:
        return None


def recipe_summary(userid, recipeid):
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
    query_ok, recipe_result = db_execute(
        recipe_sql, {"userid": userid, "recipeid": recipeid}
    )
    if query_ok:
        return recipe_result#
    else:
        return None


def recipe_foods(recipeid):
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
    query_ok, recipe_foods_results = db_execute(recipe_foods_sql, {"recipeid": recipeid})
    if query_ok:
        return recipe_foods_results.fetchall()
    else:
        return None
    

def create_recipe(userid, recipe_name, description):
    """Inserts new recipe into user_recipes 
    and returns the the ID serial of the created row."""

    sql = text("""INSERT INTO user_recipes (userid,name,description,created_ts)
                VALUES (:userid,:recipe_name,:description,NOW()) RETURNING recipeid""")  # returns the ID serial of the created row.
    
    try:
        result = db.session.execute(sql,
            {"userid": userid, "recipe_name": recipe_name, "description": description},
        )  # result is the newest id that was just created by the insert
        newest_recipeid = result.fetchone()[0]
        db.session.commit()
        return newest_recipeid
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


def add_food_to_recipe(recipeid,foodid,amount):
    sql = text("""INSERT INTO recipe_foods (recipeid,foodid,amount)
               VALUES (:recipeid,:foodid,:amount)""")
    
    return db_commit(sql, {"recipeid": recipeid,"foodid": foodid,"amount": amount})

