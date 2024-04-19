from flask import Flask, render_template, request, session
from spotify import SpotifyAPI

app = Flask(__name__)
api = SpotifyAPI()
api.setsecret()

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
    song = api.getsong()
    return render_template('radio.html', song=song)

@app.route('/auth')
def test():
    return """<a href="https://accounts.spotify.com/authorize?client_id=c5d21a01870e4fd8a36eb3e7545070fc&response_type=code&scope=user-read-playback-state,user-modify-playback-state,user-read-playback-state,user-read-currently-playing,user-read-recently-played,streaming,user-read-playback-state&redirect_uri=http://localhost:5000/callback">
        Authorize with Spotify
      </a>"""

@app.route('/callback')
def callback():
    code = request.args.get('code')
    print("\n\n\n\n\n\n")
    print(code)
    api.exchangeToken(code)
    api.savetok()
    return """<script>window.location.replace("/radio")</script>"""

@app.route("/media/play", methods=['POST'])
def play():
    api.pause()
    return "OK", 200

@app.route("/media/pause", methods=['POST'])
def pause():
    api.play()
    return "OK", 200

@app.route("/media/player", methods=['get'])
def player():
    return api.player()

if __name__ == "__main__":
    app.run(debug=True)