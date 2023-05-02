import unittest
from flask import session
from flaskr import create_app
from flaskr.db import get_db, init_db
import tempfile
from datetime import datetime

class KanbanTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

        self.app = create_app({
            'TESTING': True,
            'DATABASE': self.db_path,
        })
        with self.app.app_context():
            init_db()
            self.db = get_db()

        self.client = self.app.test_client()
        self.client.post('/auth/register',
            data={'username': 'test', 'password': 'test'}
        )

    def login(self, username='test', password='test'):
        return self.client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self.client.get('/auth/logout')

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Code Kaboodle', response.data)

    def test_board_requires_login(self):
        response = self.client.get('/board')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/board', follow_redirects=True)
        self.assertIn(b'Log In', response.data)
        

    def test_board(self):
        self.login()
        response = self.client.get('/board', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add Tasks', response.data)

    def test_create_task(self):
        self.login()
        response = self.client.post('/board', data={
            'title': 'Test Task',
            'description': 'This is a test task',
            'category': 'todo',
            'time': '2023-09-12'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Task', response.data)

    def test_update_task(self):
        self.login()
        self.client.post('/board', data={
            'title': 'Test Task',
            'description': 'This is a test task',
            'category': 'todo',
            'time': '2023-03-20'
        }, follow_redirects=True)
        response = self.client.post('/1/update?category=inprogress', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'In Progress', response.data)

    def test_delete_task(self):
        self.login()
        self.client.post('/board', data={
            'title': 'Test Task',
            'description': 'This is a test task',
            'category': 'todo',
            'time': '2023-03-20'
        }, follow_redirects=True)
        response = self.client.post('/1/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Test Task', response.data)

if __name__ == '__main__':
    unittest.main()