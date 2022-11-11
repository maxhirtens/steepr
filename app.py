from flask import Flask, request, render_template, redirect, flash, jsonify
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from auth import authentication
import requests
app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'boomerang'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///dbname"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['WTF_CSRF_ENABLED'] = False
debug = DebugToolbarExtension(app)

headers = authentication

@app.route('/')
def homepage():
  '''Show user form and embedded player.'''

  minutes = int(request.args.get('minutes', 4))
  genre = request.args.get('genre', 'folk')

  res = requests.get(f'https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track&market=US&limit=50', headers=headers)

  json = res.json()

  if 'error' in json:
    print(json['error'])

  tracks = json['tracks']['items']

  ids = []

  for item in tracks:
    name = item['name']

    artist = item['artists'][0]['name']

    id = item['id']

    duration = item['duration_ms']

    rounded_duration = round((duration/60000), 2)

    if rounded_duration >= (minutes-0.2) and rounded_duration <= (minutes+0.2):
      # print(f"'{name}' by {artist} is {rounded_duration} minutes, which is about {minutes} minutes. The id is {id}.")
      ids.append(id)

  src_id = choice(ids)
  # print(src_id)

  flash(f'You chose a {genre} song that is ~{minutes} minutes long. Press play to start steeping!')

  return render_template('index.html', src_id=src_id)
