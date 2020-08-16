import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Movie, Actor
from auth import AuthError, requires_auth

RESULTS_PER_PAGE = 10
# helper function


def paginate_results(request, selection):
    # Get page from request. 1 If not given
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    # Format selection into list
    objectsFormatted = [objectName.format() for objectName in selection]
    return objectsFormatted[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    db_drop_and_create_all()

    CORS(app)
    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'POST,GET,PATCH,DELETE,OPTIONS')
        return response

    # -- API Endpoints -- #

    # -- Movies endpoints -- #

    # /movies [GET]
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        selection = Movie.query.all()
        movies_paginated = paginate_results(request, selection)

        if len(movies_paginated) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': movies_paginated
        })

    # /movies [POST]
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def insert_movies(payload):
        # Inserts a new movie
        # Get request json
        body = request.get_json()

        if not body:
            abort(400)

        # Extract title and release_date from request body
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        # abort if title or release_date are missing
        if not title:
            abort(422)

        if not release_date:
            abort(422)

        # Create new movie & insert it.
        new_movie = (Movie(title=title, release_date=release_date))
        new_movie.insert()

        return jsonify({
            'success': True,
            'created': new_movie.id
        })

    # /movies/<movie_id> [PATCH]
    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('edit:movies')
    def edit_movies(payload, movie_id):
        # Edit an existing Movie
        # Get request json
        body = request.get_json()

        # Abort if no movie_id
        if not movie_id:
            abort(400)

        # Abort if no body has been provided
        if not body:
            abort(400)

        # Find movie by id
        movie_to_update = Movie.query.filter(
            Movie.id == movie_id).one_or_none()
        # Abort 404 if no movie with this id
        if not movie_to_update:
            abort(404)
        # Extract title and age value from request body
        title = body.get('title', movie_to_update.title)
        release_date = body.get('release_date', movie_to_update.release_date)
        # Set new field values
        movie_to_update.title = title
        movie_to_update.release_date = release_date
        # Update movie with new values
        movie_to_update.update()
        # Return success
        return jsonify({
            'success': True,
            'edited': movie_to_update.id,
            'movie': [movie_to_update.format()]
        })

    # /movies/<movie_id> [DELETE]
    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):
        # Delete an existing Movie
        # Abort if no movie_id has been provided
        if not movie_id:
            abort(400)

        # Find movie by id
        delete_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        # abort 404 If no movie with given id could found
        if not delete_movie:
            abort(404)

        # Delete movie from database
        delete_movie.delete()

        # Return success
        return jsonify({
            'success': True,
            'deleted': movie_id
        })

    # -- Actors endpoints -- #

    # /actors [GET]
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        # return all actors
        selection = Actor.query.all()
        actors_paginated = paginate_results(request, selection)

        if len(actors_paginated) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'actors': actors_paginated
        })

    # /actors [POST]

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def insert_actors(payload):
        # Inserts a new Actor
        # Get request json
        body = request.get_json()

        if not body:
            abort(400)

        # Extract name and age from request body
        name = body.get('name', None)
        age = body.get('age', None)

        # Set gender to value or to 'Other' if not given
        gender = body.get('gender', 'Other')

        # abort if name or age are missing
        if not name:
            abort(422)

        if not age:
            abort(422)

        # Create new instance of Actor & insert it.
        new_actor = (Actor(name=name, age=age, gender=gender))
        new_actor.insert()

        return jsonify({
            'success': True,
            'created': new_actor.id
        })

    # /actors/<actor_id> [PATCH]
    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('edit:actors')
    def edit_actors(payload, actor_id):
        # Edit an existing Actor
        # Get request json
        body = request.get_json()

        # Abort if no actor_id
        if not actor_id:
            abort(400)

        if not body:
            abort(400)

        # Find actor by id
        update_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        # Abort 404 if no actor with this id
        if not update_actor:
            abort(404)

        # Extract name and age value from request body, If not given, set
        # existing field
        name = body.get('name', update_actor.name)
        age = body.get('age', update_actor.age)
        gender = body.get('gender', update_actor.gender)

        # Set new field values
        update_actor.name = name
        update_actor.age = age
        update_actor.gender = gender

        # update actor with new values
        update_actor.update()

        # Return success
        return jsonify({
            'success': True,
            'updated': update_actor.id,
            'actor': [update_actor.format()]
        })

    # /actors/<actor_id> [DELETE]
    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):
        # Delete an existing Actor
        # Abort if no actor_id has been provided
        if not actor_id:
            abort(400)

        # Find actor by id
        delete_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        # If no actor with given id could found
        if not delete_actor:
            abort(404)

        # Delete actor from database
        delete_actor.delete()

        # Return success
        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    # error handlers for all expected errors
    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({"success": False, "error": 422,
                         "message": "unprocessable"}), 422)

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({"success": False, "error": 400,
                         "message": "bad request"}), 400)

    @app.errorhandler(404)
    def ressource_not_found(error):
        return (jsonify({"success": False, "error": 404,
                         "message": "resource not found"}), 404)

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return (jsonify({"success": False,
                         "error": AuthError.status_code,
                         "message": AuthError.error['description']}),
                AuthError.status_code)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
