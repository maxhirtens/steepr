'''Steep model tests.'''

# python3 -m unittest test_steep_model.py

import os
from unittest import TestCase
from models import db, User, Steep

os.environ['DATABASE_URL'] = "postgresql:///steepr-test"

from app import app

db.create_all()

class SteepModelTestCase(TestCase):
    """Test views for steeps."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u = User.signup("frank131", "password")
        db.session.commit()

        self.u = User.query.get('frank131')

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_steep_model(self):
        """Does steep model work?"""

        s = Steep(
            name="Morning Black Tea",
            genre='jazz',
            duration='5',
            username='frank131'
        )

        db.session.add(s)
        db.session.commit()

        # User should have 1 steep
        self.assertEqual(len(self.u.steeps), 1)
        self.assertEqual(self.u.steeps[0].name, "Morning Black Tea")
        self.assertEqual(self.u.steeps[0].genre, "jazz")

  def test_steep_ids(self):

    s1 = Steep(
            name="Morning Black Tea",
            genre='jazz',
            duration='5',
            username='frank131'
        )

    s2 = Steep(
            name="Evening Green Tea",
            genre='classical',
            duration='2',
            username='frank131'
        )

    db.session.add(s1)
    db.session.add(s2)
    db.session.commit()

    self.assertEqual(s1.steep_id, 1)
    self.assertEqual(s2.steep_id, 2)
