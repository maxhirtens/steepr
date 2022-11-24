"""SQLAlchemy models for Steepr."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.
    """

    db.app = app
    db.init_app(app)

class User(db.Model):
  '''User class.'''

  __tablename__ = 'users'

  username = db.Column(
        db.Text,
        primary_key=True,
        nullable=False,
        unique=True
    )

  password = db.Column(
          db.Text,
          nullable=False
      )

  steeps = db.relationship('Steep', backref='user', cascade='all, delete')

  @classmethod
  def signup(cls, username, password):
    '''sign up new user.'''

    hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

    user = User(
            username=username,
            password=hashed_pwd
        )

    db.session.add(user)
    return user

  @classmethod
  def authenticate(cls, username, password):
    """Find user with `username` and `password`."""

    user = cls.query.filter_by(username=username).first()

    if user:
        is_auth = bcrypt.check_password_hash(user.password, password)
        if is_auth:
            return user

    return False

class Steep(db.Model):
  '''Steep class.'''

  __tablename__ = 'steeps'

  steep_id = db.Column(
        db.Integer,
        primary_key=True
    )

  name = db.Column(
        db.Text,
        nullable=False
    )

  genre = db.Column(
          db.Text,
          nullable=False
      )

  duration = db.Column(
          db.Text,
          nullable=False
      )

  song_id = db.Column(
          db.Text,
          nullable=True
  )

  username = db.Column(db.Text, db.ForeignKey('users.username'), nullable=False)
