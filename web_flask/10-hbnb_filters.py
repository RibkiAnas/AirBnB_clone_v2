#!/usr/bin/python3
"""
Script that starts a Flask web application
on 0.0.0.0, port 5000.
"""

from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def states_list():
    """Displays all cities of a state and amenity in a html page"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template('10-hbnb_filters.html',
                           states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(self):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
