from db import db
from sqlalchemy.sql import text

def get_userid(username):
    sql = text("""SELECT id FROM users WHERE users.username = :username""")
    result = db.session.execute(sql,{"username":username})
    userid = result.fetchone()[0]
    print(userid)
    return userid

