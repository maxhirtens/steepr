from flask import Flask, request, render_template, redirect, flash, jsonify, session, g
from random import randint, choice
from flask_debugtoolbar import DebugToolbarExtension
import requests
from forms import SearchForm, UserAddForm
from spotipy.oauth2 import SpotifyClientCredentials
from models import db, connect_db, User, Steep
import spotipy
from dotenv import load_dotenv

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'boomerang'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///steepr"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['WTF_CSRF_ENABLED'] = True
debug = DebugToolbarExtension(app)

connect_db(app)

load_dotenv()

# *********Global Functions**********

def get_track(minutes, genre):
    '''Get matching track from Spotify API, send src id to embedded player.'''

    # Using Spotipy for Auth help
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    offset = randint(0, 100)

    result = sp.search(q='genre:' + genre, type='track',market='US',limit=50, offset=offset)

    tracks = result['tracks']['items']

    ids = []

    for item in tracks:
      name = item['name']

      artist = item['artists'][0]['name']

      id = item['id']

      duration = item['duration_ms']

      rounded_duration = round((duration/60000), 2)

      if rounded_duration >= (minutes-0.2) and rounded_duration <= (minutes+0.2):
        print(f"'{name}' by {artist} is {rounded_duration} minutes, which is about {minutes} minutes. The id is {id}.")
        ids.append(id)

    src_id = choice(ids)
    # print(src_id)

    return src_id

# *********View Functions**********

@app.route('/', methods=['GET', 'POST'])
def homepage():
  '''Show user form and embedded player.'''

  form = SearchForm()

  steeps = Steep.query.all()

  if form.validate_on_submit():
    minutes = int(form.minutes.data)
    genre = form.genre.data

    src_id = get_track(minutes, genre)

    flash(f'You chose a {genre} song that is ~{minutes} minutes long. Press play to start steeping! Your tea will be ready when the song is over.')
    return render_template('player.html', src_id=src_id, genre=genre, minutes=minutes)

  else:
    return render_template('homepage.html', form=form, steeps=steeps)

@app.route('/signup', methods=['GET', 'POST'])
def sign_user_up():
  '''Sign new user up and add to DB.'''

  form = UserAddForm()

  if form.validate_on_submit():
    user = User.signup(
      username = form.username.data,
      password = form.password.data
    )
    db.session.commit()

    return redirect('/')

  else:
    return render_template('signup.html', form=form)



@app.route('/login')
def log_user_in():
  '''Authenticate and log in user.'''
  return redirect('/')
