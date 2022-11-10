from flask import Flask, request, render_template, redirect, flash, jsonify
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
import requests
app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'boomerang'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///dbname"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['WTF_CSRF_ENABLED'] = False
debug = DebugToolbarExtension(app)

headers = {"Authorization": "Bearer BQAVOoOPYkKnPy2nd2maqCjGq4yyPZiEjCuti0XVUYsccKBDcr-KKw7eNNYkCwCSm6dsVr9_Rsbc1603TKWjWeePC9rrnVLUefU_ql3R6xAPFBbrUD7FF_MpGlIKRQVoWZfNkqUqIUuRhNp5c9PvUDexxvoptbHwHnYHXupBgAIerw4"}

@app.route('/')
def homepage():
  '''Show user form and embedded player.'''
  # minutes = 3
  # genre = 'folk'

  minutes = int(request.args.get('minutes', 4))
  genre = request.args.get('genre', 'folk')

  res = requests.get(f'https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track&market=US&limit=50', headers=headers)

  json = res.json()

  # print(json)

  tracks = json['tracks']['items']

  urls = []

  for item in tracks:
    name = item['name']

    artist = item['artists'][0]['name']

    url = item['external_urls']['spotify']

    duration = item['duration_ms']

    rounded_duration = round((duration/60000), 2)

    if rounded_duration >= (minutes-0.2) and rounded_duration <= (minutes+0.2):
      # print(f"'{name}' by {artist} is {rounded_duration} minutes, which is about {minutes} minutes. The URL is {url}.")
      urls.append(url)

  src = urls[0]
  src_id = src[-22:]

  return render_template('index.html', src_id=src_id)
