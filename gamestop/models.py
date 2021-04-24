from gamestop import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #games = db.relationship('Game', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    release = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    developers = db.Column(db.String(200), nullable=False)
    publishers = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(20), nullable=False)
