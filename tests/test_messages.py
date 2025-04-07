import unittest
from src.app import create_app

class TestMessages(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_message_without_app_key(self):
        response = self.client.post('/api/messages', json={
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'subject': 'Test',
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, 403)

    def test_create_message_success(self):
        response = self.client.post('/api/messages', json={
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'subject': 'Test',
            'message': 'Test message'
        }, headers={'X-React-App-Key': self.app.config['REACT_APP_KEY']})
        self.assertEqual(response.status_code, 201)