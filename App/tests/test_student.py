# import os, tempfile, pytest, logging, unittest
# from werkzeug.security import check_password_hash, generate_password_hash

# from App.main import create_app
# from App.database import db, create_db
# from App.models import Student
# from App.controllers import (
#     create_student,
#     get_karma,
#     get_student_by_id,
#     get_student_by_UniId,
#     get_student_by_username,
#     get_students_by_degree,
#     get_students_by_faculty,
#     get_all_students_json,
#     update_admittedTerm,
#     update_yearofStudy,
#     update_degree,
#     create_karma
# )

# LOGGER = logging.getLogger(__name__)

# '''
#    Unit Tests
# '''
# class StudentUnitTests(unittest.TestCase):

#     def test_new_student(self):
#         student = Student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5")
#         assert student.username == "billy"

#     def test_get_json(self):
#         student = Student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5")
#         karma = get_karma(student.karmaID)
#         student_json = student.to_json(karma)
#         print(student_json)
#         self.assertDictEqual(student_json, {"studentID": None,
#                                             "username": "billy",
#                                             "firstname": "Billy",
#                                             "lastname": "John",
#                                             "gpa": "3.5",
#                                             "email": "billy@example.com",
#                                             "faculty": "FST",
#                                             "degree": "BSc Computer Science",
#                                             "admittedTerm": "2022/2023",
#                                             "UniId": "816000000",
#                                             # "reviews": [],
#                                             "accomplishments": [],
#                                             "incidents": [],
#                                             "grades": [],
#                                             "transcripts": [],
#                                             "karmaScore": None,
#                                             "karmaRank": None})


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

# class StudentIntegrationTests(unittest.TestCase):

#     def test_create_student(self):
#         assert create_student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5") == True
        
#     def test_get_student_by_id(self):
#         student = get_student_by_id(1)
#         assert student is not None
    
#     def test_get_student_by_username(self):
#         student = get_student_by_username("billy")
#         assert student is not None

#     def test_get_studens_by_degree(self):
#         students = get_students_by_degree("BSc Computer Science")
#         assert students != []

#     def test_get_students_by_faulty(self):
#         students = get_students_by_faculty("FST")
#         assert students != []
    
#     def test_get_students_json(self):
#         students = get_all_students_json()
#         assert students != []

#     def test_update_admittedTerm(self):
#         assert update_admittedTerm(1, "2023/2024") == True
    
#     # def test_update_yearOfStudy(self):
#     #     assert update_yearofStudy(1, 1) == True
    
#     def test_get_student_by_UniId(self):
#       student = get_student_by_UniId("816000000")
#       assert student is not None
    
#     def test_update_degree(self):
#         assert update_degree(1, "BSc Computer Science Special") == True

#     def test_student_update(self):
#         student = Student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5")
#         create_karma(student.ID)
#         student.karmaID = get_karma(student.ID).karmaID
#         student.update(2)
#         assert get_karma(student.ID).rank == 2
        