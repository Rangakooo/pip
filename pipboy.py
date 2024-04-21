from flask import Flask, render_template

app = Flask(__name__)
print("hello")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats.html')
def stats():
    return render_template('stats.html')

@app.route('/inv.html')
def inv():
    return render_template('inv.html')

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

if __name__ == "__main__":
    app.run(debug=True)