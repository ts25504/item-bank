# -*- coding: utf-8 -*-
import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User

class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_index(self):
        response = self.client.get('/index', follow_redirects=True)
        self.assertTrue(re.search('欢迎', response.data))

