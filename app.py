import os
from flask import Flask, request, jsonify, abort, session, redirect
from sqlalchemy import exc
import json
from flask_cors import CORS
from src.auth.auth import AuthError, requires_auth, requires_signed_in
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
import constants

from src.database.models import db_drop_and_create_all, setup_db, Movie, Actor

AUTH0_CALLBACK_URL = constants.AUTH0_CALLBACK_URL
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
AUTH0_BASE_URL = 'https://' + os.environ['AUTH0_DOMAIN']
AUTH0_AUDIENCE = constants.AUTH0_AUDIENCE

app = Flask(__name__)
setup_db(app)
CORS(app)

#db_drop_and_create_all()

# ROUTES


@app.after_request
def after_request(response):

    response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

    response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
    return response

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL,
                                        audience=AUTH0_AUDIENCE)

@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint

    res = auth0.authorize_access_token()
    token = res.get('access_token')

    # Store the user information in flask session.
    session['jwt_token'] = token

    return redirect('/movies')


'''MOVIES ROUTES'''

@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(jwt):
    '''Get all movies'''
    movies = Movie.query.all()

    return jsonify({
        'success': True,
        'movies': [movie.format() for movie in movies]
    }), 200

@app.route('/movies/<int:id>', methods=['GET'])
def get_movies_by_id(id):
    '''Get a specific movie route'''
    movie = Movie.query.get(id)

    #return 404 if there is no movie with id
    if movie is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200


@app.route('/movies', methods=['POST'])
def post_movie():
    '''Create a new movie'''

    data = request.get_json()

    title = data.get('title', None)
    release_date = data.get('release_date', None)

    if title is None or release_date is None:
        abort(400)

    movie = Movie(title=title, release_date=release_date)

    try:
        movie.insert()
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 201
    except Exception:
        abort(500)

@app.route('/movies/<int:id>', methods=['PATCH'])
def patch_movie(id):
    '''Update a movie route'''

    data = request.get_json()
    title = data.get('title', None)
    release_date = data.get('release_date', None)

    movie = Movie.query.get(id)

    if movie is None:
        abort(404)

    if title is None or release_date is None:
        abort(404)

    movie.title = title
    movie.release_date = release_date

    try:
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    except Exception:
        abort(500)

@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    '''Delete a movie from table'''
    movie = Movie.query.get(id)
    
    if movie is None:
        abort(404)
    try:
        movie.delete()
        return jsonify({
            'success': True,
            'message': 'movies id {}, titled {} was deleted'.format(movie.id, movie.title)
        })
    except Exception:
        db.session.rollback()
        abort(500)



"""ACTORS ROUTES"""

@app.route('/actors', methods=['GET'])
def get_actors():
    '''Get all actors'''

    actors = Actor.query.all()

    return jsonify({
        'success': True,
        'actors': [actor.format() for actor in actors]
    }), 200

@app.route('/actors/<int:id>', methods=['GET'])
def get_actor_by_id(id):
    '''Get actor by Actor ID'''

    actor = Actor.query.get(id)

    #return 404 if Actor with ID is not present
    if actor is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

@app.route('/actors', methods=['POST'])
def post_actor():
    '''Post new Actor to the table'''

    data = request.get_json()

    name = data.get('name', None)
    age = data.get('age', None)
    gender = data.get('gender', None)

    if name is None or age is None or gender is None:
        abort(400)

    actor = Actor(name=name, age= age, gender= gender)

    try:
        actor.insert()
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 201
    
    except Exception:
        abort(500)


@app.route('/actors/<int:id>', methods=['PATCH'])
def patch_actor(id):
    '''Update a actor route'''

    data = request.get_json()
    name = data.get('name', None)
    gender = data.get('gender', None)
    age = data.get('age', None)

    actor = Actor.query.get(id)

    if actor is None:
        abort(404)

    if name is None or gender is None or age is None:
        abort(404)

    actor.name = name
    actor.gender = gender
    actor.age = age

    try:
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200
    except Exception:
        abort(500)
        

@app.route('/actors/<int:id>', methods=['DELETE'])
def delete_actor(id):
    '''Delete an Actor entry from table'''

    actor = Actor.query.get(id)

    if actor is None:
        abort(404)

    try:
        actor.delete()
        return jsonify({
            'success': True,
            'message': 'actor id {}, named {} was deleted'.format(actor.id, actor.name)
        })
    except Exception:
        db.session.rollback()
        abort(500)


    


if __name__ == "__main__":
    app.run()



