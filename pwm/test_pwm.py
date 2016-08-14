# coding:utf-8

from unittest import TestCase
from pwm import PWM
import re
import os


class TestPwm(TestCase):

    def setUp(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "tmp.dat")
        self.p = PWM(key='123456',  db_path= self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.unlink(os.path.join(os.path.dirname(__file__), "tmp.dat"))

    def test_gen_passwd(self):

        passwd = self.p.gen_passwd('1234')
        self.assertTrue(re.search(r"[0-9]", passwd) is not None)
        self.assertTrue(re.search(r"[a-z]", passwd) is not None)
        self.assertTrue(re.search(r"[A-Z]", passwd) is not None)

    def test_insert(self):
        self.p.insert(domain='github.com', account='lovedboy', batch='')
        res = self.p._query_account('github.com')
        self.assertEqual(res, [(1, 'github.com', 'lovedboy', '')])

    def test_search(self):
        self.p.insert(domain='github.com', account='lovedboy', batch='')
        self.p.search('*')

    def test_delete(self):
        self.p.insert(domain='github.com', account='lovedboy', batch='')
        res = self.p._query_account('github.com')
        self.assertEqual(res, [(1, 'github.com', 'lovedboy', '')])
        self.p.delete(1)
        res = self.p._query_account('github.com')
        self.assertEqual(res, [])

    def test_gen_account_password(self):

        p = self.p.gen_account_passwd('github.com', 'lovedboy', '')
        self.assertEqual(p, 'lcrv5vttjqOk7c3')


