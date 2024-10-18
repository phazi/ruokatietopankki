from db import db
from sqlalchemy.sql import text
from flask import redirect, session, url_for


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
    recipe_result = db.session.execute(recipe_sql, {"userid": userid})
    return recipe_result.fetchall()
