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
from models import db, User, People, Planet, Favorite
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

CURRENT_USER_ID = 1

@app.route('/users', methods=['GET'])
def get_all_users():
    response_body = User.all_users()
    if not response_body:
        return jsonify({"msg": "No users found"}), 404
    return jsonify(response_body), 200

@app.route('/user/favorites', methods=['GET'])
def get_favorites():
    user = User.query.get(CURRENT_USER_ID)
    if not user:
        return jsonify({"msg": "No user found"}), 404
    
    favorites = user.favorites
    response_body = [fav.serialize() for fav in favorites]

    return jsonify(response_body), 200

###############################
###     PEOPLE ENDPOINTS    ###
###############################

@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.get_all_people()
    if not people:
        return jsonify({"msg": "No people found"}), 400
    return jsonify(people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "No person found"}), 400
    return jsonify(person), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):
    person = People.query.get(people_id)
    add_person = Favorite(name=person.name, user_id=CURRENT_USER_ID)
    db.session.add(add_person)
    db.session.commit()
    return jsonify(add_person), 201

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people(people_id):
    person = People.query.get(people_id)
    delete_person = Favorite.query.filter_by(name=person.name).first()
    db.session.delete(delete_person)
    db.session.commit()
    return jsonify({"msg": "Person deleted"}), 200

###############################
###     PLANET ENDPOINTS    ###
###############################

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.all_planets()
    if not planets:
        return jsonify({"msg": "Planets not found"}), 400
    return jsonify(planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "No planet found"}), 400
    return jsonify(planet), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    planet = Planet.query.get(planet_id)
    add_planet = Favorite(name=planet.name, user_id=CURRENT_USER_ID)
    db.session.add(add_planet)
    db.session.commit()
    return jsonify(add_planet), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    planet = Planet.query.get(planet_id)
    delete_planet = Favorite.query.filter_by(name=planet.name).first()
    db.session.delete(delete_planet)
    db.session.commit()
    return jsonify({"msg": "Planet deleted"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
