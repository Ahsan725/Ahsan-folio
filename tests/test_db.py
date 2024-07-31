import unittest
from peewee import *
from app import TimelinePost

# Use an in-memory SQLite database for testing
test_db = SqliteDatabase(':memory:')

class TestTimeLinePost(unittest.TestCase):
    def setUp(self):
        # Bind test_db to models
        test_db.bind([TimelinePost], bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables([TimelinePost])
    
    def tearDown(self):
        test_db.drop_tables([TimelinePost])
        test_db.close()
    
    def test_timeline_post(self):
        # Create and test timeline posts
        first_post = TimelinePost.create(name='John Doe', 
                                        email='john@example.com', content='Hello world, I\'m John!')
        self.assertEqual(first_post.id, 1)
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world, I\'m Jane!')
        self.assertEqual(second_post.id, 2)

# Run the tests
if __name__ == '__main__':
    unittest.main()
