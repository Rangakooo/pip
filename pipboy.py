from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///inventory.sqlite3'

db = SQLAlchemy(app)

class inventory(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    category = db.Column(db.String(100))

    def __init__(self, name, quantity, category):
        self.name = name
        self.quantity = quantity
        self.category = category

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats.html')
def stats():
    return render_template('stats.html')

@app.route('/inv.html')
def inv():
    items = inventory.query.all()
    return render_template('inv.html', items=items)

@app.route('/data.html')
def data():
    return render_template('data.html')

@app.route('/map.html')
def map():
    return render_template('map.html')

@app.route('/radio.html')
def radio():
    return render_template('radio.html')

@app.route('/special.html')
def special():
    return render_template('special.html')


@app.route('/inv/show_all_items')
def show_all_items():
    items = inventory.query.all()
    return render_template('inv.html', items=items)

@app.route('/inv/show_items_category/<category>')
def show_items_category(category):
    items = inventory.query.filter_by(category=category).all()
    return render_template('inv.html', items=items)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)