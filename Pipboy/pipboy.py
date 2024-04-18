from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/inv')
def inv():
    return render_template('inv.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/radio')
def radio():
    return render_template('radio')

@app.route('/test')
def test():
    return render_template('main')

if __name__ == "__main__":
    app.run(debug=True)