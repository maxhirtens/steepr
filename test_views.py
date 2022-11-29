"""View tests."""

#  FLASK_ENV=production python3 -m unittest test_views.py

import os
from unittest import TestCase

from models import db, connect_db, User, Steep

os.environ['DATABASE_URL'] = "postgresql:///steepr-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class ViewTestCase(TestCase):
    """Test views."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="martin987",
                                    password="potatoes")

        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_create_steep(self):
      '''Can we add a new steep?'''

      with self.client as c:
          with c.session_transaction() as sess:
              sess[CURR_USER_KEY] = self.testuser.username
              sess['genre'] = 'jazz'
              sess['minutes'] = '5'

          resp = c.post("/savesteep", data={"name": "Tea Test"})

          self.assertEqual(resp.status_code, 302)

          # check steep name
          steep = Steep.query.one()
          self.assertEqual(steep.name, 'Tea Test')

          # check for steep in users.steeps
          self.assertEqual(len(self.testuser.steeps), 1)
          # check db for steep
          s = Steep.query.get(1)
          self.assertIsNotNone(s)

          s2 = Steep.query.get(2)
          self.assertIsNone(s2)

    def test_save_specific_steep(self):
          '''Can we add a new steep?'''

          with self.client as c:
              with c.session_transaction() as sess:
                  sess[CURR_USER_KEY] = self.testuser.username
                  sess['genre'] = 'jazz'
                  sess['minutes'] = '5'
                  sess['src_id'] = 'd48yfwe9ub74nafsiubi9'

              resp = c.post("/savespecificsteep", data={"name": "Specific Steep Test"})

              self.assertEqual(resp.status_code, 302)

              # check steep name
              steep = Steep.query.one()
              self.assertEqual(steep.name, 'Specific Steep Test')
              self.assertEqual(steep.song_id, 'd48yfwe9ub74nafsiubi9')

              # check for song_id in users.steeps
              self.assertEqual(self.testuser.steeps[0].song_id, 'd48yfwe9ub74nafsiubi9')
