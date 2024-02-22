"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites_planet, Favorites_character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    print(all_users)
    return jsonify(all_users)

@app.route('/user', methods=['POST'])
def create_user():
    request_body_user = request.get_json()
    new_user = User(email = request_body_user["email"], password = request_body_user["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(request_body_user), 200

@app.route('/user/favorites', methods=['GET'])
def get_favorites():
    favorite_planet = Favorites_planet.query.all()
    favorite_character = Favorites_character.query.all()
    planet_favorites = list(map(lambda x: x.serialize(), favorite_planet))
    character_favorites = list(map(lambda x: x.serialize(), favorite_character))
    return jsonify(planet_favorites, character_favorites), 200



@app.route('/character', methods=['GET'])
def get_people():
    characters = Character.query.all()
    all_character = list(map(lambda x: x.serialize(), characters))
    return jsonify(all_character), 200 

@app.route('/character', methods=['POST'])
def create_character():
    body = request.get_json()

    new_character = Character(
        name=body["name"],
        last_name=body["last_name"],
        gender=body["gender"],
        hair_color=body["hair_color"],
        eye_color=body["eye_color"]
    )

    db.session.add(new_character)
    db.session.commit()

    return jsonify({"message": "Character created successfully"}), 201

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_id(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify(), 404
    return jsonify(character.serialize()), 200



@app.route('/planet', methods=['GET'])
def get_planet():
    planetas = Planet.query.all()
    all_planet = list(map(lambda x: x.serialize(), planetas))
    return jsonify(all_planet), 200

@app.route('/planet', methods=['POST'])
def create_planet():
    body = request.get_json()

    new_planet = Planet(
        name=body["name"],
        diameter=body["diameter"],
        population=body["population"],
        gravity=body["gravity"],
        climate=body["climate"]
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"message": "Planet created successfully"}), 201

@app.route('/planet/<int:planets_id>', methods=['GET'])
def get_planet_id(planets_id):
    planet = Planet.query.get(planets_id)
    if planet:
        return jsonify(planet.serialize()), 200
    else:
        return jsonify({"error": "Planet not found"}), 404
    


@app.route('/favorites_planet/planet/<int:planet_id>', methods=['POST'])
def create_favorites_planet(planet_id):
    planets = Planet.query.get(planet_id)
    if planets is None:
        return  jsonify({"error"}), 404
    new_favorite = Favorites_planet(
      id_planets= planet_id,
      id_user= 1
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 200


@app.route('/favorites_character/character/<int:character_id>', methods=['POST'])
def create_favorites_people(character_id):
    people = Character.query.get(character_id)
    if people is None:
        return  jsonify({"error"}), 404
    new_favorite = Favorites_character(
      id_character= character_id,
      id_user= 1
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 200




@app.route('/favorites_planet/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    # Similar a las funciones anteriores, pero en lugar de añadir un favorito, aquí eliminas uno existente.
    favorito = Favorites_planet.query.filter_by(planet_id=planet_id).first()
    if favorito:
        db.session.delete(favorito)
        db.session.commit()
        return jsonify({"message": "Planeta eliminado"}), 200
    else:
        return jsonify({"message": "Planeta no encontrado"}), 404 



@app.route('/favorites_character/character/<int:character_id>', methods=['DELETE'])  
def delete_character_favorite(character_id):
    # Similar a las funciones anteriores, pero en lugar de añadir un favorito, aquí eliminas uno existente.
    favorito = Favorites_character.query.filter_by(character_id=character_id).first()
    if favorito:
        db.session.delete(favorito)
        db.session.commit()
        return jsonify({"message": "Personaje eliminado"}), 200
    else:
        return jsonify({"message": "Personaje no encontrado"}), 404 



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
