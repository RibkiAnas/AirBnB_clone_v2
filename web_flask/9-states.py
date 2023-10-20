#!/usr/bin/python3
"""
Script that starts a Flask web application
on 0.0.0.0, port 5000.
"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Displays all states created in a html page"""
    states = storage.all("State").values()
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):
    """Displays state by id in a html page"""
    state = None
    for st in storage.all("State").values():
        if st.id == id:
            state = st
            break

    return render_template('9-states.html', state=state)


@app.teardown_appcontext
def teardown(self):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
