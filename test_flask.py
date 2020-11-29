from unittest import TestCase

from app import app
from models import db, User

# Using test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="Jeremy", last_name="Johnson", image_url="")
        # add in a test user
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        
        user2 = User(first_name="Rishi", last_name="Sunak", image_url="")
        # add in a second test user
        db.session.add(user2)
        db.session.commit()

        self.user2_id = user2.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
    

    def test_list_users(self):
        #list all users
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jeremy', html)
            self.assertIn('Rishi', html)


    def test_show_user_details(self): 
        # user get() with user id to find user
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Jeremy Johnson</h1>', html)

    def test_show_user2_details(self): 
        # user get() with user id to find user
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user2_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Rishi Sunak</h1>', html)

    
    def test_delete_user(self):
        # delete user
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user2_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn('Rishi Sunak', html)

    
    def test_add_new_user(self):
        #add new user
         with app.test_client() as client:
            d = {"first_name": "Alkesh", "last_name": "Singh", "image_url": " "}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Alkesh Singh", html)

    




