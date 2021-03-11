import flask
from flask import request
from restocker import Restocker

api = flask.Flask(__name__)

logic = Restocker('./tables', spoiler_safe=True)

@api.route('/restock')
def restock():
    return logic.roll_traverse_table()

if __name__ == '__main__':
    api.run()
