from db import db
from sqlalchemy.sql import text
from flask import redirect, session, url_for



def food_in_fav_foods(foodid,userid):

    sql = text("""SELECT user_fav_foods.id 
               FROM user_fav_foods 
               WHERE user_fav_foods.userid = :userid
               AND user_fav_foods.foodid = :foodid
               AND active = TRUE""")
    result = db.session.execute(sql,{"foodid":foodid,"userid":userid})
    print("userid: ", userid, " foodid: ", foodid)
    return result.fetchone()

def add_fav_foood(foodid,userid):
        insert_sql = text("""INSERT INTO user_fav_foods (userid, foodid, created_ts)
                           VALUES (:userid,:foodid, NOW())""")
        db.session.execute(insert_sql, {"userid":userid,"foodid":foodid})
        db.session.commit()
        foodpage_url = url_for('foodpage',id=foodid,fav_food_added=False)
        return redirect(foodpage_url)

def my_fav_foods(userid):
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
    fav_food_results = db.session.execute(fav_food_sql,{"userid":userid})
    return fav_food_results.fetchall()