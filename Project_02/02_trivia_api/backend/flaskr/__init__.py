#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# --helper function(paginates & format question)--#

def paginate_questions(request, selection):

  # Get page from request, 1 if not given

    page = request.args.get('page', 1, type=int)

  # Calculate Start and end

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

  # Format selection into list

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

  # returns a list of questions, MAX 10Question

    return current_questions


def create_app(test_config=None):

  # create and configure the app

    app = Flask(__name__)
    setup_db(app)

  # CORS(app)

    cors = CORS(app, resources={r"/api/*": {'origins': '*'}})

  # Root Route(For Testing)

    @app.route('/')
    def hello():
        return jsonify({'message': 'HELLO'})

  # CORS Header

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():

    # get all categories

        categories = Category.query.all()

    # (404)error if no categories

        if not categories:
            abort(404)

    # Format it as list

        categories_arr = [category.format() for category in categories]

    # empty list to be filled and returned

        all_categories = []
        for category in categories_arr:
            all_categories.append(category['type'])

    # Return successfull response with list of categories

        return jsonify({'success': True,
                       'categories_arr': categories_arr,
                       'categories': all_categories})

    @app.route('/categories', methods=['POST'])
    def create_category():
        body = request.get_json()

        # Get field informations from request body

        new_type = body.get('type', None)

        # Make sure that all required fields are given.

        if not new_type:
            abort(400)

        try:

            # Try to insert a new category.

            category = Category(type=new_type)
            category.insert()

            # get all categories

            categories = Category.query.order_by(Category.id).all()
            all_categories = [category.format() for category in
                              categories]

            # Return succesfull response

            return jsonify({'success': True,
                           'categories': all_categories,
                           'created': category.id})
        except:

            abort(422)

    @app.route('/questions')
    def retrieve_questions():

    # Get all  Questions and ordered by id

        selection = Question.query.order_by(Question.id).all()

    # invoke 'paginate_questions' function

        current_questions = paginate_questions(request, selection)

    # Get and format all categories

        categories = Category.query.all()
        categories_arr = [category.format() for category in categories]

    # if There is no question

        if len(current_questions) == 0:
            abort(404)

    # empty list to append categories type

        all_categories = []
        for category in categories_arr:
            all_categories.append(category['type'])

    # return successful response

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions),
            'categories': all_categories,
            'current_category': all_categories,
            })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        # using question.id to find the correct question

        question = Question.query.filter(Question.id
                == question_id).one_or_none()

        # (404)error if there is no question

        if not question:
            abort(400)

        try:
            question.delete()

      # Get and order all Question

            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_questions(request, selection)
            return jsonify({'success': True, 'deleted': question_id,
                           'questions': current_question})
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_search_question():
        body = request.get_json()
        if not body:
            abort(400)
        search_term = body.get('searchTerm', None)

    # If json body contains  search term

        if search_term:
            questions = \
                Question.query.filter(Question.question.contains(search_term)).all()

            if not questions:
                abort(404)

      # if questions have been found, format result

            found_questions = [question.format() for question in
                               questions]

      # for total_questions

            selections = Question.query.order_by(Question.id).all()

      # query for categories and return as list

            categories = Category.query.all()
            all_categories = [category.format() for category in
                              categories]

      # successful response

            return jsonify({
                'success': True,
                'questions': found_questions,
                'total_questions': len(selections),
                'current_category': all_categories,
                })

    # Get field informations from request body, to create new question

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        try:

      # insert new question

            new_question = Question(question=question, answer=answer,
                                    category=category,
                                    difficulty=difficulty)
            new_question.insert()

      # get all paginated questions

            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_questions(request, selection)

      # successful response

            return jsonify({
                'success': True,
                'created': new_question.id,
                'questions': current_question,
                'total_questions': len(Question.query.all()),
                })
        except:
            abort(422)

    @app.route('/categories/<string:category_id>/questions',
               methods=['GET'])
    def get_questions_based_on_category(category_id):

    # query for all questions mach category_id

        selection = Question.query.filter(Question.category
                == str(category_id)).order_by(Question.id).all()

        if not selection:
            abort(400)

    # paginate and format questions

        current_question = paginate_questions(request, selection)

        if not current_question:
            abort(404)

    # successful response

        return jsonify({
            'success': True,
            'questions': current_question,
            'total_questions': len(selection),
            'current_category': category_id,
            })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        # helper function #

        def random_question(questions, previous_questions):

            # format questions

            questions = [question.format() for question in questions]

            # to choose unique question not in previous_questions

            unique_questions = [question for question in questions
                                if question['id']
                                not in previous_questions]

            # if there are no questions

            if len(unique_questions) == 0:
                return None

            # or return rondom_question with random_index

            random_index = random.randrange(0, len(unique_questions))
            rondom_question = unique_questions[random_index]
            return rondom_question

        # Get json from request

        body = request.get_json()
        try:

            # get ('previous_questions','quiz_category') from json body

            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)

            # if ALL categories

            if quiz_category['id'] == 0:

                # gut all questions from all categories.

                question_selection = Question.query.all()

                # Calling (random_question) Function
                # save the result in (next_question) variable

                next_question = random_question(question_selection,
                        previous_questions)
            else:

                # gut all questions from one category.

                question_selection = \
                    Question.query.filter(Question.category
                        == quiz_category['id']).all()

                # if there are no questions

                if len(question_selection) == 0:
                    abort(404)

                next_question = random_question(question_selection,
                        previous_questions)
        except:

            abort(422)
        return jsonify({'success': True, 'question': next_question})

  # error handlers for all expected errors

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({'success': False, 'error': 404,
                'message': 'resource not found'}), 404)

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({'success': False, 'error': 422,
                'message': 'unprocessable'}), 422)

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({'success': False, 'error': 400,
                'message': 'bad request'}), 400)

    return app
