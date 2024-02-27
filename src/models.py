from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250), nullable=True)
    population = db.Column(db.Integer, nullable=True)
    gravity = db.Column(db.String(250), nullable=True)
    climate = db.Column(db.String(250), nullable=True)
    favorites = db.relationship('Favorites', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(250), nullable=True)
    hair_color = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    favorites = db.relationship('Favorites', backref='character', lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.name

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)

    def __repr__(self):
        return "<Favorites user_id=%r, character_id=%r, planet_id=%r>" % (self.user_id, self.character_id, self.planet_id)