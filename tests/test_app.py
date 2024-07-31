import unittest
import os
from app import app, TimelinePost
from peewee import SqliteDatabase
os.environ['TESTING'] = 'true'

from app import app

# Use an in-memory SQLite database for testing
test_db = SqliteDatabase(':memory:')

class AppTestCase(unittest.TestCase):
    def setUp(self):
          # Bind test_db to models and initialize the Flask test client
        test_db.bind([TimelinePost], bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables([TimelinePost])

        # Set up Flask application for testing
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def tearDown(self):
        # Clean up after each test
        test_db.drop_tables([TimelinePost])
        test_db.close()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<h1>MLH Fellow</h1>" in html
        assert "About" in html
        
    def test_timeline(self):
        # response = self.client.get("/api/timeline_post")
        # assert response.status_code == 200
        # assert response.is_json
        # json = response.get_json()
        # assert "timeline_posts" in json
        # assert len(json["timeline_posts"]) == 0
        # def test_timeline(self):
        # Test the GET endpoint
        response = self.client.get("/api/timeline_post")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        json_data = response.get_json()
        self.assertIn("timeline_posts", json_data)
        self.assertEqual(len(json_data["timeline_posts"]), 0)  # Expecting an empty list

        
    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html
        
        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html
        
        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

