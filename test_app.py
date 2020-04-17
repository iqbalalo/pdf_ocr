import unittest
from app import app


class TestCase(unittest.TestCase):

    def test_index(self):
        app.testing = True
        tester = app.test_client()
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()