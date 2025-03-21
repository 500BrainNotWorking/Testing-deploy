import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_username,
    update_email,
    update_faculty,
    update_name,
    update_password,
    
    create_student,
    get_karma,
    get_student_by_id,
    get_student_by_UniId,
    get_student_by_username,
    get_students_by_degree,
    get_students_by_faculty,
    get_all_students_json,
    update_admittedTerm,
    update_yearofStudy,
    update_degree,
    create_karma
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User(username="bob", firstname="Bob", lastname="Smith", password="bobpass", email="bob@example.com", faculty="FST")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User(username="bob", firstname="Bob", lastname="Smith", password="bobpass", email="bob@example.com", faculty="FST")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "firstname":"Bob", "lastname":"Smith", "email":"bob@example.com", "faculty":"FST"})

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User(username="bob", firstname="Bob", lastname="Smith", password=password, email="bob@example.com", faculty="FST")
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User(username="bob", firstname="Bob", lastname="Smith", password=password, email="bob@example.com", faculty="FST")
        assert user.check_password(password)


class StudentUnitTests(unittest.TestCase):

    def test_new_student(self):
        student = Student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5")
        assert student.username == "billy"

    # def test_get_json(self):
    #     student = Student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5")
    #     karma = get_karma(student.karmaID)
    #     student_json = student.to_json(karma)
    #     print(student_json)
    #     self.assertDictEqual(student_json, {"studentID": None,
    #                                         "username": "billy",
    #                                         "firstname": "Billy",
    #                                         "lastname": "John",
    #                                         "gpa": "3.5",
    #                                         "email": "billy@example.com",
    #                                         "faculty": "FST",
    #                                         "degree": "BSc Computer Science",
    #                                         "admittedTerm": "2022/2023",
    #                                         "UniId": "816000000",
    #                                         # "reviews": [],
    #                                         "accomplishments": [],
    #                                         "incidents": [],
    #                                         "grades": [],
    #                                         "transcripts": [],
    #                                         "karmaScore": None,
    #                                         "karmaRank": None})

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "Bob", "Smith", "bobpass", "bob@example.com", "FST")
    assert login("bob", "bobpass") != None

class UserIntegrationTests(unittest.TestCase):

    # def test_get_all_users_json(self):
    #     #user = create_user("rick", "Rick", "Grimes", "rickpass", "rick@example.com", "FST")
    #     users_json = get_all_users_json()
    #     self.assertListEqual([{"id":1, 
    #         "username":"bob", 
    #         "firstname":"Bob", 
    #         "lastname":"Smith", 
    #         "email":"bob@example.com", 
    #         "faculty":"FST"},
    #         {
    #         "id":2, 
    #         "username":"rick", 
    #         "firstname":"Rick", 
    #         "lastname":"Grimes", 
    #         "email":"rick@example.com", 
    #         "faculty":"FST"
    #         }], users_json)

    def test_create_user(self):
        user = create_user("rick", "Rick", "Grimes", "rickpass", "rick@example.com", "FST")
        assert user.username == "rick"


    # Tests data changes in the database
    def test_update_user(self):
        update_username(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

    def test_update_name(self):
        update_name(1, "Bobby", "Jones")
        user = get_user(1)
        assert user.firstname == "Bobby"
        assert user.lastname == "Jones"

    def test_update_email(self):
        update_email(1, "newemail@example.com")
        user = get_user(1)
        assert user.email == "newemail@example.com"

    def test_update_password(self):
        update_password(1, "newpass")
        user = get_user(1)
        assert user.check_password("newpass")

    def test_update_faculty(self):
        update_faculty(1, "New Faculty")
        user = get_user(1)
        assert user.faculty == "New Faculty"


# class StudentIntegrationTests(unittest.TestCase):

#      def test_create_student(self):
#         assert create_student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5") == True
        

class StudentIntegrationTests(unittest.TestCase):

    def test_create_student(self):
        assert create_student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5") == True
        
    # def test_get_student_by_id(self):
    #     create_student(username="willy", firstname="Willy", lastname="Fohn", email="willy@example.com", password="willypass", faculty="FST", admittedTerm="2022/2023", UniId="816000001", degree="BSc Computer Science", gpa="2.5")
    #     student = get_student_by_id(1)

    #     print (student.username)
    #     assert student.username == "willy"
    
    def test_get_student_by_name(self):
        create_student(username="Jae", firstname="Jae", lastname="Son", email="jae@example.com", password="jaepass", faculty="FST", admittedTerm="2022/2023", UniId="816000002", degree="BSc Computer Science", gpa="2.7")
        student = get_student_by_username("Jae")
        assert student is not None

    def test_get_studens_by_degree(self):
        students = get_students_by_degree("BSc Computer Science")
        assert students != []

    def test_get_students_by_faulty(self):
        students = get_students_by_faculty("FST")
        assert students != []
    
    def test_get_students_json(self):
        students = get_all_students_json()
        assert students != []

    # def test_update_admittedTerm(self):
    #     assert update_admittedTerm(1, "2023/2024") == True
    
    # # def test_update_yearOfStudy(self):
    # #     assert update_yearofStudy(1, 1) == True
    
    def test_get_student_by_UniId(self):
      student = get_student_by_UniId("816000000")
      assert student is not None
    
    # def test_update_degree(self):
    #     assert update_degree(1, "BSc Computer Science Special") == True
