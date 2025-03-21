# import os, tempfile, pytest, logging, unittest
# from werkzeug.security import check_password_hash, generate_password_hash

# from App.main import create_app
# from App.database import db, create_db
# from App.models import Karma
# # from App.controllers import (
# #     get_karma,
# #     create_karma,
# #     calculate_review_points,
# #     update_review_points
# # )

# '''
#    Unit Tests
# '''
# class KarmaUnitTests(unittest.TestCase):

#     def test_new_karma(self):
#         newKarma = Karma(points=0.0, academicPoints=0.0, accomplishmentPoints=0.0, reviewsPoints=0.0,incidentPoints=0.0, rank=-99, studentID = 1)
#         assert newKarma is not None

#     def test_karma_to_json(self):
#         newKarma = Karma(points=0.0, academicPoints=0.0, accomplishmentPoints=0.0, reviewsPoints=0.0,incidentPoints=0.0, rank=-99, studentID = 1)
#         newKarma_json = newKarma.to_json()
#         self.assertDictEqual(newKarma_json,{
#             "karmaID": None,
#             "score": 0.0,
#             "academicPoints": 0.0, 
#             "accomplishmentPoints": 0.0, 
#             "reviewPoints": 0.0,
#             "incidentPoints": 0.0,
#             "rank": -99,
#             "studentID": 1
#         })
# '''
#     Integration Tests
# '''

# # This fixture creates an empty database for the test and deletes it after the test
# # scope="class" would execute the fixture once and resued for all methods in the class
# @pytest.fixture(autouse=True, scope="module")
# def empty_db():
#     app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
#     create_db()
#     yield app.test_client()
#     db.drop_all()

# class KarmaIntegrationTests(unittest.TestCase):

#     def test_create_karma(self):
#         assert create_karma(1) == True

#     def test_get_karma(self):
#         self.test_create_karma()
#         karma = get_karma(1)
#         assert karma.studentID == 1

#     def test_calculate_karma(self):
#         karma = calculate_review_points(1)
#         assert karma == 0

#     def test_update_karma(self):
#         assert update_review_points(1) == True

#     def test_karma_notify(self):
#         karma = get_karma(1)
        
#         assert karma.notify() == True