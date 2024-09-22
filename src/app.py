from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///postgres"
db = SQLAlchemy(app)



@app.route("/foodpage/<int:id>")
def page(id):
    sql = text("SELECT foodname FROM food WHERE foodid = (:id)")
    result = db.session.execute(sql,{"id":id})
    food_name = result.fetchone()
    return "Tämä on sivu " + str(id) + " eli " + food_name.foodname



class Food(db.Model):
    """This class acts as mapping between database object and Python code"""

    foodid = db.Column(db.Integer, primary_key=True)
    edport = db.Column(db.Integer)
    foodtype = db.Column(db.String)
    process = db.Column(db.String)
    fuclassp = db.Column(db.String)
    igclass = db.Column(db.String)
    igclassp = db.Column(db.String)
    fuclass = db.Column(db.String)
    foodname = db.Column(db.String)

    def to_dict(self):
        return {
            'foodid': self.foodid,
            'edport': self.edport,
            'foodtype': self.foodtype,
            'process': self.process,
            'fuclassp': self.fuclassp,
            'igclass': self.igclass,
            'igclassp': self.igclassp,
            'fuclass': self.fuclass,
            'foodname': self.foodname
        }


@app.route('/')
def index():
    return render_template('server_table.html')

@app.route('/api/data')
def data():
    query = Food.query

    # search filter:

    # below row parses the URL parameters (returns the part after question mark).
    # in this case it returns the value after ?search=
    search = request.args.get('search') 
    if search:
        query = query.filter(db.or_(
            Food.foodname.ilike(f'%{search}%'),
            Food.foodtype.ilike(f'%{search}%')
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in ['foodname', 'foodtype']:
                name = 'foodname'
            col = getattr(Food, name)
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
        'data': [food.to_dict() for food in query],
        'total': total,
    }

if __name__ == '__main__':
    app.run()