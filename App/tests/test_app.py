import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Staff, Review, Comment, Reply, Karma
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
    create_karma,

    create_staff,
    get_staff_by_id,
    get_staff_by_username,
    staff_create_review,
    staff_edit_review,
    create_student,
    get_student_by_username,
    get_review,

    create_student,
    create_staff,
    get_staff_by_username,
    get_staff_by_id,
    get_student_by_id,
    get_student_by_username,
    create_review,
    delete_review_work,
    edit_review_work,
    get_review
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


class StaffUnitTests(unittest.TestCase):

    def test_new_staff(self):
        staff = Staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST")
        assert staff.username == "joe"

    def test_get_json(self):
        staff = Staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST")
        staff_json = staff.to_json()
        print(staff_json)
        self.assertDictEqual(staff_json, {"staffID": None,
            "username": "joe",
            "firstname": "Joe",
            "lastname": "Mama",
            "email": "joe@example.com",
            "faculty": "FST",
            "reviews": [],
            "reports": [],
            "pendingAccomplishments": []})


class ReviewUnitTests(unittest.TestCase):

    def test_new_review(self):
        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
        assert create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031160',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("billy")
        staff = get_staff_by_username("joe")
        review = Review(staff, student, 3, "Billy is good.")
        assert review is not None

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
    #     #create_student(username="willy", firstname="Willy", lastname="Fohn", email="willy@example.com", password="willypass", faculty="FST", admittedTerm="2022/2023", UniId="816000001", degree="BSc Computer Science", gpa="2.5")
    #     student = get_student_by_id(5)

    #     expected_student = {
    #             "username":"billy", 
    #             "firstname":"Billy", 
    #             "lastname":"John", 
    #             "email":"billy@example.com", 
    #             "faculty":"FST", 
    #             "admittedTerm":"2022/2023", 
    #             "UniId":"816000000", 
    #             "degree":"BSc Computer Science", 
    #             "gpa":"3.5"
    #     }
    #     self.assertEqual(student.username, expected_student["username"])
    #     self.assertEqual(student.firstname, expected_student["firstname"])
    #     self.assertEqual(student.lastname, expected_student["lastname"])
    #     self.assertEqual(student.email, expected_student["email"])
    #     self.assertEqual(student.faculty, expected_student["faculty"])
    #     self.assertEqual(student.admittedTerm, expected_student["admittedTerm"])
    #     self.assertEqual(student.UniId, expected_student["UniId"])
    #     self.assertEqual(student.degree, expected_student["degree"])
    #     self.assertEqual(student.gpa, expected_student["gpa"])
    
    def test_get_student_by_name(self):
        create_student(username="Jae", firstname="Jae", lastname="Son", email="jae@example.com", password="jaepass", faculty="FST", admittedTerm="2022/2023", UniId="816000002", degree="BSc Computer Science", gpa="2.7")
        student = get_student_by_username("Jae")
        assert student.username == "Jae"

    def test_get_studens_by_degree(self):
        create_student(username="Jae", firstname="Jae", lastname="Son", email="jae@example.com", password="jaepass", faculty="FST", admittedTerm="2022/2023", UniId="816000002", degree="BSc Computer Science (Special)", gpa="2.7")
        students = get_students_by_degree("BSc Computer Science (Special)")

        expected_student = {
                "username":"Jae", 
                "firstname":"Jae", 
                "lastname":"Son", 
                "email":"jae@example.com", 
                "faculty":"FST", 
                "admittedTerm":"2022/2023", 
                "UniId":"816000002", 
                "degree":"BSc Computer Science (Special)", 
                "gpa":"2.7"
        }
        self.assertEqual(students[0].username, expected_student["username"])
        self.assertEqual(students[0].firstname, expected_student["firstname"])
        self.assertEqual(students[0].lastname, expected_student["lastname"])
        self.assertEqual(students[0].email, expected_student["email"])
        self.assertEqual(students[0].faculty, expected_student["faculty"])
        self.assertEqual(students[0].admittedTerm, expected_student["admittedTerm"])
        self.assertEqual(students[0].UniId, expected_student["UniId"])
        self.assertEqual(students[0].degree, expected_student["degree"])
        self.assertEqual(students[0].gpa, expected_student["gpa"])

    def test_get_students_by_faulty(self):
        create_student(username="Ryan", firstname="Ryan", lastname="Aire", email="ryan@example.com", password="ryanpass", faculty="FSS", admittedTerm="2022/2023", UniId="816000005", degree="Psychology", gpa="3.7")
        students = get_students_by_faculty("FSS")
        
        expected_student = {
                "username":"Ryan", 
                "firstname":"Ryan", 
                "lastname":"Aire", 
                "email":"ryan@example.com", 
                "faculty":"FSS", 
                "admittedTerm":"2022/2023", 
                "UniId":"816000005", 
                "degree":"Psychology", 
                "gpa":"3.7"
        }
        self.assertEqual(students[0].username, expected_student["username"])
        self.assertEqual(students[0].firstname, expected_student["firstname"])
        self.assertEqual(students[0].lastname, expected_student["lastname"])
        self.assertEqual(students[0].email, expected_student["email"])
        self.assertEqual(students[0].faculty, expected_student["faculty"])
        self.assertEqual(students[0].admittedTerm, expected_student["admittedTerm"])
        self.assertEqual(students[0].UniId, expected_student["UniId"])
        self.assertEqual(students[0].degree, expected_student["degree"])
        self.assertEqual(students[0].gpa, expected_student["gpa"])
    
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


class StaffIntegrationTests(unittest.TestCase):

    def test_create_staff(self):
        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True

    def test_get_staff_by_id(self):
        create_staff(username="tyrell",firstname="Tyrell", lastname="John", email="tyrell@example.com", password="tyrellpass", faculty="FST")
        staff = get_staff_by_id(1)
        assert staff.ID == 1

    def test_get_staff_by_name(self):
        staff = get_staff_by_username("joe")
        assert staff.username == "joe"



class ReviewIntegrationTests(unittest.TestCase):

    def test_create_review(self):
        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
        assert create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031160',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("billy")
        staff = get_staff_by_username("joe")
        review1 = create_review(staff=staff, student=student, starRating=3, details="Billy is Amazing.")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":3, 
                "details":"Billy is Amazing."
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])


    def test_get_review(self):
        self.test_create_review()
        review = get_review(2)
        #print(review.to_json(student=get_student_by_id(review.studentID), staff=get_staff_by_id(review.createdByStaffID)))
        assert review is not None

    # def test_calc_points_upvote(self):
    #     self.test_create_review()
    #     review = get_review(1)
    #     print(review.to_json(student=get_student_by_id(review.studentID), staff=get_staff_by_id(review.createdByStaffID)))
    #     assert review is not None
    #     assert calculate_points_upvote(review) == True

    # def test_calc_points_downvote(self):
    #     self.test_create_review()
    #     review = get_review(1)
    #     print(review.to_json(student=get_student_by_id(review.studentID), staff=get_staff_by_id(review.createdByStaffID)))
    #     assert review is not None
    #     assert calculate_points_downvote(review) == True

    # # Test for total starRating of positive reviews
    # def test_get_total_positive_review_starRating(self):
    #     self.test_create_review()  # Assuming this creates both positive and negative reviews
    #     review = get_review(1)
    #     total_positive = get_total_positive_review_starRating(review.studentID)
    #     assert total_positive >= 0  # Ensure the total is non-negative

    # # Test for total starRating of negative reviews
    # def test_get_total_negative_review_starRating(self):
    #     self.test_create_review()  # Assuming this creates both positive and negative reviews
    #     review = get_review(1)
    #     total_negative = get_total_negative_review_starRating(review.studentID)
    #     assert total_negative >= 0  # Ensure the total is non-negative

    def test_delete_review(self):
        # self.test_create_review()

        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031166',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        delete_review_work(review.ID, staff.ID)

        deleted_review = get_review(review.ID)
        assert deleted_review is None

    
    def test_delete_review2(self):
        # self.test_create_review()

        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031166',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        wrong_id = staff.ID + 1

        delete_review_work(review.ID, wrong_id)

        deleted_review = get_review(review.ID)
        assert deleted_review is not None

