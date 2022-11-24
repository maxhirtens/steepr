"""SQLAlchemy models for Steepr."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
  '''User class.'''

  __tablename__: 'users'

  user_id = db.Column(
        db.Integer,
        primary_key=True
    )

  username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

  password = db.Column(
          db.Text,
          nullable=False
      )

  steeps = db.Column(
          db.Integer,
          db.ForeignKey('steeps.steep_id', ondelete='CASCADE')
      )

  @classmethod
  def signup(cls, username, password):
    '''sign up new user.'''

    hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

    user = User(
            username=username,
            email=email,
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

  __tablename__: 'steeps'

  steep_id = db.Column(
        db.Integer,
        primary_key=True
    )

  username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

  password = db.Column(
          db.Text,
          nullable=False
      )
