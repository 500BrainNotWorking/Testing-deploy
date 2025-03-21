# import os, tempfile, pytest, logging, unittest
# from werkzeug.security import check_password_hash, generate_password_hash

# from App.main import create_app
# from App.database import db, create_db
# from App.models import Grades
# from App.controllers import(
#     create_grade,
#     delete_grade,
#     get_grade
# )

# '''
#    Unit Tests
# '''
# class GradesUnitTests(unittest.TestCase):

#     def test_new_grade(self):
#         newGrade = Grades(studentID=1 ,course="COMP1601", grade="A")
#         assert newGrade is not None
    


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

# class GradesIntegrationTests(unittest.TestCase):

#     def test_create_grade(self):
#         assert create_grade(studentID=1, course="COMP1601", grade="A") == True
    
#     def test_delete_grade(self):
#         self.test_create_grade()
#         to_delete = get_grade(1)
#         assert to_delete is not None

#         db.session.delete(to_delete)
#         db.session.commit()

#         check = get_grade(1)

#         assert check is None
