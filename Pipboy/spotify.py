import requests
import base64
import json

class SpotifyAPI():
    def __init__(self):
        self.client_id = 'c5d21a01870e4fd8a36eb3e7545070fc'
        self.client_secret = 'f2b4622dbf8944c3a1f6d614186f0900'
        self.access_token = None
        self.refresh_token = None
        self.baseurl = 'https://api.spotify.com/v1/me/player'
        
    def setsecret(self):
        with open('secrets.json', 'r') as f:
            secrets = json.load(f)
            self.client_secret = secrets["secret"]
        

    def settoks(self, access_token, refresh_token):
        self.access_token = access_token
        if refresh_token:
            self.refresh_token = refresh_token
        

    def exchangeToken(self,code):
        auth  = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("utf-8")
        url = 'https://accounts.spotify.com/api/token'
        payload = {
            'code': code, 
            'redirect_uri': 'http://localhost:5000/callback',  
            'grant_type': 'authorization_code'}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            "Authorization": f"Basic {auth}" 
        }
        r = requests.post(url, data=payload, headers=headers)
        if r.status_code == 200:
            access_token = r.json()['access_token']
            refresh_token = r.json()['refresh_token']
            self.settoks(access_token, refresh_token)

    def refreshtok(self):
        auth  = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("utf-8")
        url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            "Authorization": f"Basic {auth}" 
        }
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        r = requests.post(url, headers=headers, data=payload)

        if r.status_code == 200:
            access_token = r.json()['access_token']
            try:
                refresh_token = r.json()['refresh_token']
            except KeyError:
                refresh_token = None
            self.settoks(access_token, refresh_token)
            
    def savetok(self):        
        with open('tokens.json', 'w') as f:
            json.dump({'access_token': self.access_token, 'refresh_token': self.refresh_token}, f)

    def loadtok(self):
        with open('tokens.json', 'r') as f:
            tokens = json.load(f)
            self.settoks(tokens['access_token'], tokens['refresh_token'])

    def nextSong(self):
        url = f"{self.baseurl}/next"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        r = requests.post(url, headers=headers)

        if r.status_code == 401:
            self.refreshtok()
            
        else:
            return r.status_code

    def prevSong(self):
        url = f'{self.baseurl}previous'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json' 
        }
        r = requests.post(url, headers=headers)

        if r.status_code == 401:
            self.refreshtok()
        else:
            return True

    def pause(self):
        url = f'{self.baseurl}/pause'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json' 
        }
        r = requests.put(url, headers=headers)
        if r.status_code == 401:
            self.refreshtok()
    
    def play(self):
        url = f"{self.baseurl}/play"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json' 
        }
        r = requests.put(url, headers=headers)
        if r.status_code == 401:
            self.refreshtok()

    def getsong(self):
        url = f'{self.baseurl}/currently-playing'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json' 
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:  
            
            return r.json()["item"]["name"]
        elif r.status_code == 401:
            self.refreshtok()
        return str(r.status_code)

    def playbackstatus(self):
        url = self.baseurl
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json' 
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()['is_playing']
        elif r.status_code == 401:
            self.refreshtok()