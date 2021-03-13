import flask
from flask import request, Response, render_template
from restocker import Restocker


api = flask.Flask(__name__)

logic = Restocker('./tables', spoiler_safe=True)

@api.route('/restock')
def restock():
    lvl = int(request.args.get('lvl', default=1))
    return Response(logic.roll_traverse_table(party_level=lvl), content_type='text/plain')

@api.route('/')
def ui():
    return render_template('index.html')

if __name__ == '__main__':
    api.run('0.0.0.0', debug=True)
