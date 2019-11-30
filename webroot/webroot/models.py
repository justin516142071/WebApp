from webroot import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60),unique=False, nullable=False)
    fc2 = db.Column(db.String(11), unique=False,nullable=False)
    currentLoginTime = db.Column(db.String(100),unique=False, nullable=True)
    queries = db.relationship('Query', backref='user', lazy=True)
    histories = db.relationship('History', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    querytext = db.Column(db.String(1000),unique=False, nullable=False)
    queryresults = db.Column(db.String(1000), unique=False, nullable=False)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    logintime = db.Column(db.String(100),unique=False, nullable=True)
    logouttime = db.Column(db.String(100), unique=False, nullable=True)