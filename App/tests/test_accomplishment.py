# import os, tempfile, pytest, logging, unittest
# from werkzeug.security import check_password_hash, generate_password_hash

# from App.main import create_app
# from App.database import db, create_db
# from App.models import Accomplishment
# from App.controllers import(
#     create_accomplishment,
#     delete_accomplishment,
#     get_accomplishments_by_studentID,
#     get_accomplishment,
#     create_student,
#     create_staff,
#     get_student_by_username,
#     get_staff_by_username,get_student_by_id
# )

# '''
#    Unit Tests
# '''
# class AccomplishmentUnitTests(unittest.TestCase):

#     def test_new_accomplishment(self):
#         assert create_student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5") == True
#         student = get_student_by_username("billy")
#         newAccomplishment = Accomplishment(student=student ,verified=False, taggedStaffId=2, details="I won first place in Runtime", points=5, topic="First place in Runtime", status="Not yet Checked",
#                                      studentSeen=False)
#         assert newAccomplishment is not None


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


# class AccomplishmentIntegrationTests(unittest.TestCase):

#     def test_create_accomplishment(self):
#       assert create_student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5") == True

#       assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True

#       student = get_student_by_username("billy")
#       staff = get_staff_by_username("joe")

#       assert create_accomplishment(studentID=student.ID, verified=False, taggedStaffName=(staff.firstname+" "+staff.lastname), details="I won first place in Runtime", points=5, topic="First in Runtime", status="Not yet Checked" ) == True

#     def test_delete_accomplishment(self):
#         self.test_create_accomplishment()
#         student = get_student_by_username("billy")
#         accomplishments = get_accomplishments_by_studentID(student.ID)
#         to_delete = accomplishments[0]
#         db.session.delete(to_delete)
#         db.session.commit()
#         check = get_accomplishment(to_delete.id)

#         assert check is None