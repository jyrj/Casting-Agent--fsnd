import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from src.database.models import db_drop_and_create_all, setup_db, Movie, Actors
#from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

#db_drop_and_create_all()

# ROUTES

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()

    return jsonify({
        'success': True,
        'movies': [movie.movies_model() for movie in movies]
    }), 200
