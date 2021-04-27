from unittest import TestCase
from app import app
from models import db, connect_db, User
from seed import seed_db

class FlaskTests(TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:myPassword@localhost:5432/blogly'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ECHO'] = True
        seed_db()

        connect_db(app)
        db.create_all()

        cls.client = app.test_client()
        with cls.client as client:
            pass

    def test_home(self):
        resp = self.client.get('/', follow_redirects=True)
        html = resp.get_data(as_text=True)
        #check if status code 200
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Users</h1>', html)

    def test_create(self):
        resp = self.client.post('/users/new', data={
            'first-name': 'Brad',
            'last-name': 'Pitt',
            'image-url': ''
        }, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<div class="h1">Brad Pitt</div>', html)

    def test_read(self):
        resp = self.client.get('/users/4', follow_redirects=True)
        html = resp.get_data(as_text=True)
        #check if status code 200
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<div class="h1">Brad Pitt</div>', html)

    def test_update(self):
        resp = self.client.post('/users/4/edit', data={
            'first-name': 'Angelina',
            'last-name': 'Jolie',
            'image-url': ''
        }, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<div class="h1">Angelina Jolie</div>', html)


    def test_delete(self):
        resp = self.client.post('/users/1/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('>John Smith</a>', html)
    
    @classmethod
    def tearDownClass(cls):
        seed_db()
