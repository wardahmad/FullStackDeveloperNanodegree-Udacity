import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, db_drop_and_create_all
from datetime import date
from sqlalchemy import desc

# Create dict with Authorization key and Bearer token as values.

casting_assistant_header_auth = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw2S1JxeDUwcTA4LXY4azdIb3Z1bSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQ1MDUwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjI2OTYyMzMxYmVkNTAwOTkwNDI2YjciLCJhdWQiOiJjYXN0aW5nQWdlbmN5IiwiaWF0IjoxNTk2MzY0MzkwLCJleHAiOjE1OTYzNzE1OTAsImF6cCI6IkR0TWtSZnpaajZFVUFrc1B3NFRHV0U3Tm9adlFnRlpkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.d5fPoM_-rrID66OOt0zVgllJN6Awxqbs5XyHGk06bf4h95DX5eCEl2I7Kpj7LDd_41QnPEv5bf_1fB53lR23qS3X-Q4xv453rN_h3Fw3Qw0bCW8a8uSaIA26pcy4O8nrdpP7cQNBARwiywZLzTKuen1foLhOZJv2qhXh5Ti4acsPLwyW_-W6nCfcwWoKeK3S8Zxf03lq3Bsk0PIXDnnI3WJqGe0EUFpwRyTtnaufHI_HCUWgpfJzVIP49G21A2glnJXtj0lxKDAmObeGeaDb6mheYU3-ar5L0_p6PitjSyxmSWy4rCQ9YD7ZoYb3GJAd23zU-hEptkBq8up3H6wscQ'
}

casting_director_header_auth = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw2S1JxeDUwcTA4LXY4azdIb3Z1bSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQ1MDUwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjI2OTZiMTI1N2IwMDAwMzhlNDU1ZDgiLCJhdWQiOiJjYXN0aW5nQWdlbmN5IiwiaWF0IjoxNTk2MzY0NTI2LCJleHAiOjE1OTYzNzE3MjYsImF6cCI6IkR0TWtSZnpaajZFVUFrc1B3NFRHV0U3Tm9adlFnRlpkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZWRpdDphY3RvcnMiLCJlZGl0Om1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.EHjiZwaxiTBLbADHw_Bp0GKLGpIBHyGZXDgD6eqyOFmwoEuSHuVJ_q8YX7lG-T7rR9QuJS3rs0BhGvZRVouI3MZx4KVpHIYEUiUhqMLdJtW7Kse2cYnHgFGd7aK7wxrB8zh1CywDreEasMs6C9AkCwKOD7jCcb_fftP8qgMfEQoG_cjRxWL-ytyI-8riT6ELf5C9pNr5bhbkaDCnRltrSl3gYxOv5mcmkNMwzE6VBj1UH-5i7ns6rTeudVLEPx4AKK3QGlkfJcdat-rSXij3IghbN_F2-1ajkDR2UX-H7bnZeIIoIeDCULyFK0om6FjfiEtjA952g77kchd_UL00_Q'
}

executive_producer_header_auth = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw2S1JxeDUwcTA4LXY4azdIb3Z1bSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQ1MDUwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjI2OTc1MzI1N2IwMDAwMzhlNDU1ZGEiLCJhdWQiOiJjYXN0aW5nQWdlbmN5IiwiaWF0IjoxNTk2MzY0Njg2LCJleHAiOjE1OTYzNzE4ODYsImF6cCI6IkR0TWtSZnpaajZFVUFrc1B3NFRHV0U3Tm9adlFnRlpkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.cieBx3MCggeF_pQRa828IMqSypfo2atDp_WUIK4vUY8C3XetyyQHUBMosdPzIbo5dqs2vy70Oc26a-rbkwUzPgBr_MgQVoCj7kF0_pFP7rdTdQDFkPhZykWOKQg7p0CS5UUi4848ZhhSRyHX6VERk-arLo5EniAs5rnOO4uLoFVpo-5bzDivl4C6fuHGh0mrFF2XBZwHVp73JYczfborYvJp7vK7MVJC6le5brJJ2d1Y1bXaDbuso57s6PGMSbWNKixleGxA_c_OlPOmDP5Wd7HhW8rNsLag2SuNXB06oX2bgsgBY94z5s3eOPDdICVDAf0ibVtM4iHc7PxhrV9vGQ'
}

# os.environ['DATABASE_URL'] = 'postgresql://postgres:1234@localhost:5432/postgres'


class AgencyTestCase(unittest.TestCase):
    # This class represents the agency test case

    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        # Executed after reach test
        pass

    # --testcases-- #

    # /movies [POST]
    def test_create_movie(self):
        create_movie = {
            'title': 'Ward Movie',
            'release_date': date.today()
        }

        res = self.client().post('/movies', json=create_movie,
                                 headers=executive_producer_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)

    def test_422_create_new_movie(self):
        create_movie = {
            'release_date': date.today()
        }

        res = self.client().post('/movies', json=create_movie,
                                 headers=executive_producer_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    # /movies GET
    def test_get_all_movies(self):
        res = self.client().get('/movies?page=1',
                                headers=casting_assistant_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_401_get_all_movies(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_404_get_movies(self):
        res = self.client().get(
            '/movies?page=22222222',
            headers=casting_assistant_header_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # /movies [PATCH]
    def test_edit_movie(self):
        edit_movie = {
            'release_date': date.today()
        }
        res = self.client().patch('/movies/1', json=edit_movie,
                                  headers=executive_producer_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)

    def test_400_edit_movie(self):
        res = self.client().patch('/movies/1',
                                  headers=executive_producer_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_404_edit_movie(self):
        edit_movie = {
            'release_date': date.today()
        }
        res = self.client().patch(
            '/movies/444444',
            json=edit_movie,
            headers=executive_producer_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # /movies [DELETE]
    def test_401_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_403_delete_movie(self):
        res = self.client().delete('/movies/1',
                                   headers=casting_assistant_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_movie(self):
        res = self.client().delete('/movies/1',
                                   headers=executive_producer_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_404_delete_movie(self):
        res = self.client().delete('/movies/55555',
                                   headers=executive_producer_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # /actors [GET]
    def test_get_all_actors(self):
        res = self.client().get('/actors?page=1',
                                headers=casting_assistant_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_error_401_get_all_actors(self):
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_error_404_get_actors(self):
        res = self.client().get(
            '/actors?page=555555',
            headers=casting_assistant_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        #self.assertEqual(data['message'] , 'resource not found')

    # /actors [POST]
    def test_create_new_actor(self):
        new_actor = {
            'name': 'Ward Ahmad',
            'age': 555
        }

        res = self.client().post('/actors', json=new_actor,
                                 headers=casting_director_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)

    def test_error_401_new_actor(self):
        create_actor = {
            'name': 'wardah',
            'age': 555
        }

        res = self.client().post('/actors', json=create_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_error_422_create_new_actor(self):
        create_actor_without_name = {
            'age': 555
        }

        res = self.client().post(
            '/actors',
            json=create_actor_without_name,
            headers=casting_director_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    # /actors [PATCH]
    def test_edit_actor(self):
        edit_actor = {
            'age': 123
        }
        res = self.client().patch('/actors/1', json=edit_actor,
                                  headers=casting_director_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        self.assertEqual(data['updated'], 1)

    def test_400_edit_actor(self):
        res = self.client().patch('/actors/5555',
                                  headers=casting_director_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_404_edit_actor(self):
        edit_actor = {
            'age': 77
        }
        res = self.client().patch(
            '/actors/66666',
            json=edit_actor,
            headers=casting_director_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # /actors [DELETE]
    def test_401_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_403_delete_actor(self):
        res = self.client().delete('/actors/1',
                                   headers=casting_assistant_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_actor(self):
        res = self.client().delete('/actors/1',
                                   headers=casting_director_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/5555',
                                   headers=casting_director_header_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


if __name__ == "__main__":
    unittest.main()
