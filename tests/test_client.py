# -*- coding: utf-8 -*-
import re
import unittest
from app import create_app, db


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

    def test_get_login(self):
        response = self.client.get('/auth/login', follow_redirects=True)
        self.assertTrue(re.search('登录', response.data))

    def test_get_logout(self):
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertTrue(re.search('您已经注销', response.data))

    def test_get_index(self):
        response = self.client.get('/index', follow_redirects=True)
        self.assertTrue(re.search('欢迎', response.data))

    def test_get_about(self):
        response = self.client.get('/about', follow_redirects=True)
        self.assertTrue(re.search('关于', response.data))

    def test_get_single_choice(self):
        response = self.client.get('/single_choice', follow_redirects=True)
        self.assertTrue(re.search('单选题', response.data))

    def test_get_blank_fill(self):
        response = self.client.get('/blank_fill', follow_redirects=True)
        self.assertTrue(re.search('填空题', response.data))

    def test_get_essay(self):
        response = self.client.get('/essay', follow_redirects=True)
        self.assertTrue(re.search('问答题', response.data))

    def test_get_test_paper(self):
        response = self.client.get('/test_papers', follow_redirects=True)
        self.assertTrue(re.search('试卷管理', response.data))

    def test_get_manage(self):
        response = self.client.get('/manage/0', follow_redirects=True)
        self.assertTrue(re.search('题库管理', response.data))
