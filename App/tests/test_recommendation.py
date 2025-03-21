# import os, tempfile, pytest, logging, unittest
# from werkzeug.security import check_password_hash, generate_password_hash

# from App.main import create_app
# from App.database import db, create_db
# from App.models import Recommendation

# from App.controllers import (
#     create_recommendation,
#     get_recommendations_student,
#     get_recommendations_staff,
#     approve_recommendation, 
#     create_student,
#     get_student_by_username,
#     get_student_by_id,
#     get_student_by_UniId
# )

# '''
#    Unit Tests
# '''
# class RecommendationUnitTests(unittest.TestCase):

#     def test_new_recommendation(self):
#         create_student(username="billy",
#                             firstname="Billy",
#                             lastname="John",
#                             email="billy@example.com",
#                             password="billypass",
#                             faculty="FST",
#                             admittedTerm="",
#                             UniId="816031160",
#                             degree="",
#                             gpa="")
#         student = get_student_by_UniId("816031160")
#         recommendation = Recommendation(student, staffID=1, approved=False, status="pending", currentYearOfStudy=2,
#                details="yeh", studentSeen=False)
#         assert recommendation is not None

#     def test_recommendation_to_json(self):
#         create_student(username="billy",
#                             firstname="Billy",
#                             lastname="John",
#                             email="billy@example.com",
#                             password="billypass",
#                             faculty="FST",
#                             admittedTerm="",
#                             UniId="816031160",
#                             degree="",
#                             gpa="")
#         student = get_student_by_UniId("816031160")
#         recommendation = Recommendation(student, staffID=1, approved=False, status="pending", currentYearOfStudy=2,
#                details="yeh", studentSeen=False)
#         rec_json = recommendation.get_json()
#         self.assertDictEqual(rec_json,{
#             'studentID': "816031160",
#             "name": "Billy John",
#             'staffID': 1,
#             'approved': False,
#             "date requested": recommendation.dateRequested.strftime("%d-%m-%Y %H:%M"),
#             "status": "pending",
#             "currentYearOfStudy": 2,
#             "details": "yeh"
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


# class RecommendationIntegrationTests(unittest.TestCase):



#     def test_create_recommendation(self):
#         create_student(username="billy",
#                             firstname="Billy",
#                             lastname="John",
#                             email="billy@example.com",
#                             password="billypass",
#                             faculty="FST",
#                             admittedTerm="",
#                             UniId="816031160",
#                             degree="",
#                             gpa="")
#         assert create_recommendation(1, staffID=1, approved=False, status="Pending", currentYearOfStudy=2,
#                details="yeh") == True

#     def test_get_recommendation_staff(self):
#         assert get_recommendations_staff(1) != []

#     def test_get_recommendation_student(self):
#         assert get_recommendations_student("816031160") != []

#     def test_approve_recommendation(self):
#         self.test_create_recommendation()
#         assert approve_recommendation(1) == True

