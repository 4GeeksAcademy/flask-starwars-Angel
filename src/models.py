from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=False)
    favorite = db.Column(db.String()), db.ForeignKey

    def __repr__(self):
        return '<User %r>' % self.username 

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    diameter = db.Column(db.String(250), nullable=True)
    population = db.Column(db.Integer)
    gravity = db.Column(db.String(250))
    climate = db.Column(db.String(250))

    def __repr__(self):
        return '<Planet %r>' % self.name 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "population": self.population,
            "gravity": self.gravity,
            "climate": self.climate,
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    __tablename__ = 'characters'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))

    def __repr__(self):
        return '<Character %r>' % self.name 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey ("user.id"),  nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey ("characters.id"), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey ("planets.id"), nullable=True)
    def __repr__(self):
        return "<Favorites %r>" % self.id   
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }