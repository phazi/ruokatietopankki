from db import db
from sqlalchemy.sql import text
from flask import redirect, session, url_for



def food_in_fav_foods(foodid,userid):

    sql = text("""SELECT user_fav_foods.id 
               FROM user_fav_foods 
               WHERE user_fav_foods.userid = :userid
               AND user_fav_foods.foodid = :foodid""")
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

