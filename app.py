import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .src.database.models import db_drop_and_create_all, setup_db, Movie, Actor
#from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

#db_drop_and_create_all()

# ROUTES

'''MOVIES ROUTES'''

@app.route('/movies', methods=['GET'])
def get_movies():
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




