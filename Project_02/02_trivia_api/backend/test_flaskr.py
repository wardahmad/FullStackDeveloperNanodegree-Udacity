#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):

    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client

        # self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

        self.database_path = \
            'postgresql://postgres:1234@localhost:5432/postgres'
        setup_db(self.app, self.database_path)

        self.new_questions = {
            'question': 'question1',
            'answer': 'answerQ1',
            'category': '1',
            'difficulty': 3,
            }

        # binds the app to the current context

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables

            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""

        pass

    def test_404_get_categories(self):

        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_categories(self):

        create_category = {'type': 'math'}
        res = self.client().post('/categories', json=create_category)
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_questions)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_400_create_question(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_404_create_question(self):
        res = self.client().post('/questions',
                                 json={'searchTerm': 'ward'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['total_questions'])

    def test_404_get_questions(self):
        res = self.client().get('/questions?page=5000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        create_question = {
            'question': 'this is q1',
            'answer': 'answer q1',
            'category': '1',
            'difficulty': 1,
            }
        res = self.client().post('/questions', json=create_question)
        data = json.loads(res.data)
        question_id = data['created']

        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_get_questions_based_on_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_400_get_questions_based_on_category(self):
        res = self.client().get('/categories/10000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_play_quiz(self):
        json_quizz = {'previous_questions' : [],
            'quiz_category' : {'type' : 'math', 'id' : '1'}}
        res = self.client().post('/quizzes', json=json_quizz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_422_play_quiz(self):
        json_quizz = {'previous_questions' : None,
            'quiz_category' : {'type' : 'quiz', 'id' : '5000'}}
        res = self.client().post('/quizzes', json=json_quizz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable

if __name__ == '__main__':
    unittest.main()
