from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, Length

# class SearchForm(FlaskForm):
#   '''Search for song with genre and duration.'''

#   genre = SelectField('Genre',
#     choices = [('rock', 'Rock'), ('jazz', 'Jazz'), ('folk', 'Folk'), ('punk', 'Punk'), ('classical', 'Classical')],
#     validators=[InputRequired()]
#     )
#   minutes = SelectField('Minutes',
#     choices = [('2', '2m'), ('3', '3m'), ('4', '4m'), ('5', '5m'), ('6', '6m')],
#     validators=[InputRequired()]
#     )

class UserAddForm(FlaskForm):
  '''Add new user to DB.'''

  username = StringField('Username', validators=[InputRequired()])
  password = PasswordField('Password', validators=[InputRequired()])

class LoginForm(FlaskForm):
  '''Log in if valid.'''

  username = StringField('Username', validators=[InputRequired()])
  password = PasswordField('Password', validators=[InputRequired()])

class SteepAddForm(FlaskForm):
  '''Add new steep to DB.'''

  name = StringField('Name', validators=[InputRequired()])
