from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from db import Food_stats, db, Food

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///postgres"
db.init_app(app)



@app.route("/foodpage/<int:id>")
def page(id):
    sql = text("SELECT foodname FROM food WHERE foodid = (:id)")
    result = db.session.execute(sql,{"id":id})
    food_name = result.fetchone()
    return "Tämä on sivu " + str(id) + " eli " + food_name.foodname

@app.route('/')
def index():
    return render_template('all_foods_table.html')

@app.route('/api/data')
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
    app.run()