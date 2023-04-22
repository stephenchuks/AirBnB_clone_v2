#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask, render_template, jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception):
    """
    Removes the current SQLAlchemy Session.
    """
    storage.close()


@app.route('/hbnb')
def hbnb():
    """
    Displays a HTML page like 8-index.html.
    """
    states = sorted(list(storage.all(State).values()), key=lambda x: x.name)
    amenities = sorted(list(storage.all(Amenity).values()), key=lambda x: x.name)
    places = sorted(list(storage.all(Place).values()), key=lambda x: x.name)

    return render_template('100-hbnb.html',
                           states=states,
                           amenities=amenities,
                           places=places)


@app.route('/states/<state_id>')
def state(state_id):
    """
    Displays a HTML page like 9-states.html.
    """
    state = storage.get(State, state_id)
    if state is None:
        return render_template('404.html')

    cities = sorted(list(state.cities), key=lambda x: x.name)

    return render_template('9-states.html',
                           state=state,
                           cities=cities)


@app.route('/cities/<city_id>')
def city(city_id):
    """
    Displays a HTML page like 9-cities.html.
    """
    city = storage.get(City, city_id)
    if city is None:
        return render_template('404.html')

    places = sorted(list(city.places), key=lambda x: x.name)

    return render_template('9-cities.html',
                           city=city,
                           places=places)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Displays a HTML page like 10-hbnb_filters.html.
    """
    states = sorted(list(storage.all(State).values()), key=lambda x: x.name)
    amenities = sorted(list(storage.all(Amenity).values()), key=lambda x: x.name)

    return render_template('10-hbnb_filters.html',
                           states=states,
                           amenities=amenities)


@app.route('/api/v1/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending on the JSON in the request.
    """
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    places = storage.all(Place).values()

    if 'states' in data:
        state_ids = data['states']
        places = [place for place in places if place.state_id in state_ids]

    if 'cities' in data:
        city_ids = data['cities']
        places = [place for place in places if place.city_id in city_ids]

    if 'amenities' in data:
        amenity_ids = data['amenities']
        places = [place for place in places if all(amenity.id in
                                                   [a.id for a in place.amenities]
                                                   for amenity in amenity_ids)]

    places = sorted(list(places), key=lambda x: x.name)

    return jsonify([place])
