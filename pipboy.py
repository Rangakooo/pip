from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///pipboy.db'

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

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    points = db.Column(db.Integer)

class Special(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Integer, nullable=False)

class Perks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    max_level = db.Column(db.Integer, nullable=False)

    def __init__(self, name, level):
        self.name = name
        self.level = level

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    icon = db.Column(db.String(255), nullable=False)

@app.route('/update_level', methods=['POST'])
def update_level():
    data = request.get_json()
    stat_name = data.get('stat')
    level_change = data.get('levelChange')

    # Query the database to find the stat
    stat = Special.query.filter_by(name=stat_name).first()

    if stat:
        # Update the level
        stat.level += level_change
        db.session.commit()
        return jsonify(stat.level)  # Return the updated level
    else:
        return jsonify({'error': 'Stat not found'}), 404

@app.route('/update_perk_level', methods=['POST'])
def update_perk_level():
    data = request.get_json()
    stat_name = data.get('stat')
    level_change = data.get('levelChange')

    # Query the database to find the stat
    stat = Perks.query.filter_by(name=stat_name).first()

    if stat:
        # Update the level
        stat.level += level_change
        db.session.commit()
        return jsonify(stat.level)  # Return the updated level
    else:
        return jsonify({'error': 'Stat not found'}), 404

@app.route('/get_user_points', methods=['GET'])
def get_user_points():
    # Assuming you have a user object, you can retrieve the points value
    user = User.query.filter_by(user_id=1).first()
    print(user)
    return jsonify({'points': user.points})

@app.route('/template.html')
def template():
    users = User.query.all()
    return render_template('template.html', users=users)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats.html')
def stats():
    users = User.query.all()
    return render_template('stats.html', users=users)

@app.route('/inv.html')
def inv():
    items = inventory.query.all()
    return render_template('inv.html', items=items)

@app.route('/perks.html')
def perks():
    perks = Perks.query.all()
    return render_template('perks.html', perks=perks)

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
    special = Special.query.all()
    return render_template('special.html', special=special)


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