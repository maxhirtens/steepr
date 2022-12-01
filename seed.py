'''Seed database for testing.'''

from app import app
from models import User, Steep, db

db.drop_all()
db.create_all()

u1 = User.signup(username='tom121', password='tomatoes')
u2 = User.signup(username='barry151', password='potatoes')
u3 = User.signup(username='linda761', password='tomatoes')

db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.commit()

s1 = Steep(name='Evening Green Tea', genre='classical', duration='2', username='tom121')
s2 = Steep(name='Morning English Breakfast', genre='folk', duration='5', username='tom121')
s3 = Steep(name='Afternoon Rooibos', genre='jazz', duration='3', username='tom121')
s4 = Steep(name='Morning Oolong', genre='punk', duration='4', username='linda761', song_id='0rOTMSSa6yscfOrGnzfheM')

db.session.add(s1)
db.session.add(s2)
db.session.add(s3)
db.session.add(s4)
db.session.commit()
