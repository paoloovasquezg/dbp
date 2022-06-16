import unittest

from server import create_app
from models import setup_db, Usuario, Radio, RadioUsuario
import json


class TestCaseTodoApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'test'
        self.database_path='postgresql://{}:{}@{}/{}'.format('postgres','1234', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        res = self.client().get('/usuarios')
        data = json.loads(res.data)

        if data['success'] != True:
            self.client().post('/radiosusuarios', json={'name': 'sofia'})

    def test_get_usuarios_success(self):
        self.client().post('/usuarios', json={'name': 'sofia'})
        res = self.client().get('/usuarios')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_usuarios'])
        self.assertTrue(len(data['usuarios']))

    def test_get_radios_success(self):
        self.client().post('/radios', json={'name': 'sofia'})
        res = self.client().get('/radios')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_radios'])
        self.assertTrue(len(data['radios']))

    def test_get_radiousers_success(self):
        self.client().post('/usuarios', json={'name': 'sofia'})
        self.client().post('/radios', json={'name': 'sofia'})

        res = self.client().get('/radiosusuarios')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_radiosusuarios'])
        self.assertTrue(len(data['radiosusuarios']))

    def test_create_usuario_success(self):
        res = self.client().post('/usuarios', json={'name':'sofia'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['usuarios']))
        self.assertTrue(data['total_usuarios'])

    def test_create_radio_success(self):
        res = self.client().post('/radios', json={'name':'sofia'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['radios']))
        self.assertTrue(data['total_radios'])

    def test_create_radiousuario_success(self):
        res = self.client().post('/radiosusuarios', json={'name': 'sofia'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_radiosusuarios'])
        self.assertTrue(len(data['radiosusuarios']))

    
    def tearDown(self):
        pass