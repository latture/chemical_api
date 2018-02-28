import base64
import json
import unittest
from pymongo import MongoClient
from chemical_api import app, DoNotUseInProductionAuth


class TestApp(unittest.TestCase):
    def setUp(self):
        self.mongo_host = 'localhost'
        self.mongo_port = 27017
        self.mongo_dbname = 'test_eve'
        self.mongo_username = None
        self.mongo_password = None

        self.app = app
        self.app.config['MONGO_HOST'] = self.mongo_host
        self.app.config['MONGO_PORT'] = self.mongo_port 
        self.app.config['MONGO_DBNAME'] = self.mongo_dbname 
        self.test_client = self.app.test_client()

        self.known_resource_url = '/chemicals'

        self.valid_chemical = {
            'formula': 'test',
            'band_gap': 0.0,
            'color': 'test',
        }
        self.invalid_chemical = {}

        self.setupDB()
    
        self.content_type = ('Content-Type', 'application/json')
        self.valid_auth = self.create_auth_headers('admin', 'admin')
        self.invalid_auth = self.create_auth_headers('nope', 'nope')
        self.app.set_defaults()

    def tearDown(self):
        del self.app
        self.dropDB()

    def setupDB(self):
        self.connection = MongoClient(self.mongo_host, self.mongo_port)
        self.connection.drop_database(self.mongo_dbname)
        if self.mongo_username:
            self.connection[self.mongo_dbname].add_user(self.mongo_username, self.mongo_password)

    def dropDB(self):
        self.connection = MongoClient(self.mongo_host, self.mongo_port)
        self.connection.drop_database(self.mongo_dbname)
        self.connection.close()

    def create_auth_headers(self, username, password):
        credentials = base64.b64encode(bytes(f'{username}:{password}', 'ascii')).decode('ascii')
        return [('Authorization', f'Basic {credentials}'), self.content_type]

    def test_custom_auth(self):
        self.assertTrue(isinstance(self.app.auth, DoNotUseInProductionAuth))

    def test_unauthorized_get_access(self):
        r = self.test_client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_unauthorized_post_access(self):
        r = self.test_client.post(self.known_resource_url,
                                  headers=self.invalid_auth)
        self.assertEqual(r.status_code, 401)

    def test_authorized_post_access(self):
        r = self.test_client.post(self.known_resource_url,
                                  headers=self.valid_auth)
        self.assertEqual(r.status_code, 400)

    def test_valid_post(self):
        r = self.test_client.post(self.known_resource_url,
                                  data=json.dumps(self.valid_chemical),
                                  headers=self.valid_auth)
        self.assertEqual(r.status_code, 201)

    def test_invalid_post(self):
        r = self.test_client.post(self.known_resource_url,
                                  data=json.dumps(self.invalid_chemical),
                                  headers=self.valid_auth)
        self.assertEqual(r.status_code, 422)
