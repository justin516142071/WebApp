import random
import unittest
from webroot import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


class FlaskTestCase(unittest.TestCase):
    """ This is one of potentially many TestCases """

    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
        db = SQLAlchemy(app)
        bcrypt = Bcrypt(app)
        login_manager = LoginManager(app)
        self.app = app.test_client()

    def test_route_register(self):
        res = self.app.get("/register")
        # print(dir(res), res.status_code)
        assert res.status_code == 200

    def test_route_login(self):
        res = self.app.get("/login")
        assert res.status_code == 200

    def test_route_spell_check(self):
        res = self.app.get("/spell_check")
        assert res.status_code == 401

   # def test_route_loginacc(self):
   #     #res = self.app.post("/login", data={'uname': 'easyeasyacc', 'pword': '123456', '2fa': '1234567890'})
   #     res = self.app.post("/login",data={'uname':'easyeasyacc','pword':'123456','2fa':'1234567890'},follow_redirects=True)
   #     print(res.status_code)
   #     res = self.app.get("/spell_check")
   #     assert 'Failure' in res.data.decode("utf-8")

if __name__ == '__main__':
    unittest.main()
