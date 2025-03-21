# import os, tempfile, pytest, logging, unittest
# from werkzeug.security import check_password_hash, generate_password_hash

# from App.main import create_app
# from App.database import db, create_db
# from App.models import Staff
# from App.controllers import (
#     create_staff,
#     get_staff_by_id,
#     get_staff_by_username,
#     staff_create_review,
#     staff_edit_review,
#     create_student,
#     get_student_by_username,
#     get_review
# )
# '''
#    Unit Tests
# '''
# class StaffUnitTests(unittest.TestCase):

#     def test_new_staff(self):
#         staff = Staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST")
#         assert staff.username == "joe"

#     def test_get_json(self):
#         staff = Staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST")
#         staff_json = staff.to_json()
#         print(staff_json)
#         self.assertDictEqual(staff_json, {"staffID": None,
#             "username": "joe",
#             "firstname": "Joe",
#             "lastname": "Mama",
#             "email": "joe@example.com",
#             "faculty": "FST",
#             "reviews": [],
#             "reports": [],
#             "pendingAccomplishments": []})


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

# class StaffIntegrationTests(unittest.TestCase):

#     def test_create_staff(self):
#         assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True

#     def test_get_staff_by_id(self):
#         staff = get_staff_by_id(1)
#         assert staff is not None

#     def test_get_staff_by_username(self):
#         staff = get_staff_by_username("joe")
#         assert staff is not None

#     def test_staff_create_review(self):
#         assert create_student(username="billy",
#                  firstname="Billy",
#                  lastname="John",
#                  email="billy@example.com",
#                  password="billypass",
#                  faculty="FST",
#                  admittedTerm="",
#                  UniId='816031160',
#                  degree="",
#                  gpa="") == True
#         student = get_student_by_username("billy")
#         staff = get_staff_by_id(1)
#         assert staff is not None
#         assert staff_create_review(staff, student, 3, "Billy is good.") == True

#     def test_staff_edit_review(self):
#         review = get_review(1)
#         assert review is not None
#         assert staff_edit_review(review.ID, "Billy is very good") == True