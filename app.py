from flask import Flask, request, render_template, redirect, flash, jsonify, session, g
from random import randint, choice
from flask_debugtoolbar import DebugToolbarExtension
import requests
from forms import UserAddForm, LoginForm, SteepAddForm
from spotipy.oauth2 import SpotifyClientCredentials
from models import db, connect_db, User, Steep
import spotipy
from pprint import pprint
from dotenv import load_dotenv

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'boomerang'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///steepr"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['WTF_CSRF_ENABLED'] = True
debug = DebugToolbarExtension(app)

CURR_USER_KEY = "curr_user"

connect_db(app)

load_dotenv()

# *********Global Functions**********

# Using Spotipy for Auth help
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def get_track(minutes, genre):
    '''Get matching track from Spotify API, send src id to embedded player.'''

    print(f'getting track for {genre} - {minutes}')

    offset = randint(0, 200)

    if genre:
      result = sp.search(q='genre:' + genre, type='track',market='US',limit=50, offset=offset)
    else:
      result = sp.search(q='%s%', type='track',market='US',limit=50, offset=offset)

    tracks = result['tracks']['items']

    ids = []

    for item in tracks:
      name = item['name']

      artist = item['artists'][0]['name']

      id = item['id']

      duration = item['duration_ms']

      rounded_duration = round((duration/60000), 2)

      if rounded_duration >= (minutes-0.2) and rounded_duration <= (minutes+0.2):
        ids.append(id)

    src_id = choice(ids)

    return src_id


def get_track_from_src(src_id):
  '''This is for the steep info page. It gets a track name from the src_id in session.'''

  track = sp.track(src_id)
  return track

# *********User Login Functions**********

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.username

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

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

    do_login(user)

    return redirect('/')

  else:
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def log_user_in():
  '''Authenticate and log in user.'''
  form = LoginForm()

  if form.validate_on_submit():
    user = User.authenticate(form.username.data, form.password.data)

    if user:
      do_login(user)
      flash(f"Hello, {user.username}!", "success")
      return redirect('/')

  return render_template('login.html', form=form)


@app.route('/logout')
def log_user_out():
  '''Log user out, remove from session.'''

  do_logout()
  flash(f"You have logged out!", "success")
  return redirect('/')

# *********View Functions**********

@app.route('/', methods=['GET'])
def homepage():
  '''Show track search form.'''

  steeps = Steep.query.order_by(Steep.steep_id.desc()).limit(5)

  return render_template('homepage.html', steeps=steeps)

@app.route('/player', methods=['GET', 'POST'])
def show_player():
  '''Shows player to begin steeping.'''
  form = SteepAddForm()

  minutes = int(request.args.get('minutes'))
  session['minutes'] = minutes

  genre = request.args.get('genre')
  session['genre'] = genre

  try:
    src_id = get_track(minutes, genre)
    session['src_id'] = src_id
    flash(f'Press play to start steeping! Your tea will be ready when the song is over.')
    return render_template('player.html', src_id=src_id, genre=genre, minutes=minutes, form=form)

  except:
    flash("No matching tracks, let's use another genre or time.", 'error')
    return redirect('/')

@app.route('/player/<int:steep_id>', methods=['GET', 'POST'])
def show_player_for_saved_steep(steep_id):
  '''This is a second version of the player to play saved steeps with a specific track saved.'''
  steep = Steep.query.get(steep_id)
  print(steep.duration, steep.genre)
  minutes=steep.duration
  genre=steep.genre

  if steep.song_id:
    print(steep.song_id)
    src_id = steep.song_id
  else:
    src_id = get_track(int(minutes), genre)

  flash(f'Press play to start steeping! Your tea will be ready when the song is over.')
  return render_template('player2.html', src_id=src_id, genre=genre, minutes=minutes)

@app.route('/savesteep', methods=['GET', 'POST'])
def add_steep():
  '''add a steep to db.'''

  form = SteepAddForm()

  user = User.query.get(session[CURR_USER_KEY])
  if form.validate_on_submit():

        steep = Steep(name=form.name.data, genre=session['genre'], duration=session['minutes'])
        user.steeps.append(steep)
        db.session.commit()
        flash('Steep saved')

        return redirect('/')

  flash('Something went wrong, please try again')
  return redirect('/')

@app.route('/savespecificsteep', methods=['GET', 'POST'])
def add_specific_steep():
  '''add a steep to db.'''

  form = SteepAddForm()

  user = User.query.get(session[CURR_USER_KEY])
  if form.validate_on_submit():

        steep = Steep(name=form.name.data, genre=session['genre'], duration=session['minutes'], song_id=session['src_id'])
        user.steeps.append(steep)
        db.session.commit()
        flash('Steep saved')

        return redirect('/')

  flash('Something went wrong, please try again')
  return redirect('/')

@app.route('/steeps/<int:steep_id>')
def show_steep_info(steep_id):
  '''Show steep info, option to send it back to player.'''

  steep = Steep.query.get_or_404(steep_id)

  session['minutes'] = steep.duration
  session['genre'] = steep.genre
  session['src_id'] = steep.song_id

  track_title = ''
  artist = ''

  if session['src_id'] is not None:
    track = get_track_from_src(session['src_id'])
    track_title = track['name']
    artist = track['artists'][0]['name']

  return render_template('steep.html', steep=steep, track_title=track_title, artist=artist)
