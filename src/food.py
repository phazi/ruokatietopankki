
from sqlalchemy.sql import text
from flask import redirect, url_for
from db import db, db_execute

def get_food_stats(foodid):
    """Fetches details of one specific food"""

    sql = text("""SELECT foodid
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
               WHERE foodid = (:foodid)""")
    return db_execute(sql, {"foodid": foodid})  # returns query_ok and result


def food_in_fav_foods(foodid, userid):
    """Function checks whether user has already added food as favourite"""

    sql = text("""SELECT user_fav_foods.id
               FROM user_fav_foods
               WHERE user_fav_foods.userid = :userid
               AND user_fav_foods.foodid = :foodid
               AND active = TRUE""")
    query_ok, result = db_execute(sql, {"foodid": foodid, "userid": userid})
    return result.fetchone()


def add_fav_foood(foodid, userid):
    """Adds food as user's favourite in user_fav_foods table"""

    insert_sql = text("""INSERT INTO user_fav_foods (userid, foodid, created_ts)
                           VALUES (:userid,:foodid, NOW())""")
    db.session.execute(insert_sql, {"userid": userid, "foodid": foodid})
    db.session.commit()
    foodpage_url = url_for("foodpage", foodid=foodid, fav_food_added=False)
    return redirect(foodpage_url)


def my_fav_foods(userid):
    """Fetches user's favourite foods with food statistics"""

    fav_food_sql = text("""SELECT food_stats.foodid
               ,food_stats.foodname
               ,ROUND(energia_laskennallinen,1)      as energia_laskennallinen
               ,ROUND(kcal,1)                        as kcal
               ,ROUND(rasva,1)                       as rasva
               ,ROUND(hiilihydraatti_imeytyva,1)     as hiilihydraatti_imeytyva
               ,ROUND(proteiini,1)                   as proteiini
               ,ROUND(alkoholi,1)                    as alkoholi

               FROM user_fav_foods
               INNER JOIN food_stats ON user_fav_foods.foodid = food_stats.foodid
               WHERE userid = (:userid) AND active = TRUE""")
    fav_food_results = db.session.execute(fav_food_sql, {"userid": userid})
    return fav_food_results.fetchall()


def get_foodids():
    """"Fetches all foodids and returns a list"""

    sql = text("SELECT foodid FROM food_stats GROUP BY foodid ORDER BY foodid")
    query_ok, result = db_execute(sql, {})
    if query_ok:
        return [r[0] for r in result.fetchall()]
    else:
        return None
