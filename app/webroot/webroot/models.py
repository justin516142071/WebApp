from webroot import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    fc2 = db.Column(db.String(6), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"