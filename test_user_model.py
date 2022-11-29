'''User model tests.'''

# python3 -m unittest test_user_model.py

import os
from unittest import TestCase
from models import db, User, Steep

os.environ['DATABASE_URL'] = "postgresql:///steepr-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("tommy765", "tomatoes")

        u2 = User.signup("erin545", "potatoes")

        db.session.commit()

        u1 = User.query.get('tommy765')
        u2 = User.query.get('erin545')

        self.u1 = u1
        self.u2 = u2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

# Established user testing.
    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "eggplant"))
        self.assertFalse(User.authenticate(self.u2.username, "eggplant"))

    def test_right_password(self):
        self.assertTrue(User.authenticate(self.u1.username, "tomatoes"))
        self.assertTrue(User.authenticate(self.u2.username, "potatoes"))

    def test_authentication(self):
        u = User.authenticate(self.u1.username, 'tomatoes')
        self.assertIsNotNone(u)

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("tomatoes", "tomatoes"))

# New user signup testing.
    def test_new_signup(self):
      new_user = User.signup('terry654', 'tomatoes')
      db.session.commit()

      new_user = User.query.get('terry654')
      self.assertIsNotNone(new_user)
      self.assertEqual(new_user.username, 'terry654')
      self.assertNotEqual(new_user.password, 'tomatoes')
      self.assertTrue(new_user.password.startswith("$2b$"))
      # Make sure new users have no steeps.
      self.assertEqual(len(new_user.steeps), 0)

    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("email@email.com", "")

        with self.assertRaises(ValueError) as context:
            User.signup("email@email.com", None)
