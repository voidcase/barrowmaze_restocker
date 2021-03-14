import flask
from flask import request, Response, render_template, send_from_directory
from restocker import Restocker
import math
import os



api = flask.Flask(__name__)
api.static_folder = './static'
try:
    spoiler_safe = bool(int(os.environ.get('BARROWMAZE_SPOILER_SAFE', default=1)))
except ValueError:
    print('bad value for environment variable BARROWMAZE_SPOILER_SAFE. should be 0 or 1')
    print('setting spoiler_safe to True')
    spoiler_safe = True

logic = Restocker('./tables', spoiler_safe=spoiler_safe)

@api.route('/restock')
def restock():
    try:
        lvl = int(request.args.get('lvl', default=1))
        lvl = min(max(10, lvl), 1)
    except ValueError:
        return "Hello there! Are you trying to pentest my thing by entering weird data?\n" + \
                "That's nice. Come help me inprove it at https://github.com/voidcase/barrowmaze_restocker :)"
    return Response(logic.roll_traverse_table(party_level=lvl), content_type='text/plain')

@api.route('/')
def ui():
    return render_template('index.html')

@api.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(api.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    api.run('0.0.0.0', debug=True)
