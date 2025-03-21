# import os, tempfile, pytest, logging, unittest
# from werkzeug.security import check_password_hash, generate_password_hash

# from App.main import create_app
# from App.database import db, create_db
# from App.models import IncidentReport
# from App.controllers import (
#     create_incident_report,
#     delete_incident_report,
#     create_student,
#     create_staff,
#     get_student_by_username,
#     get_staff_by_username,
#     get_incident_reports,
#     get_incident_report
# )


# '''
#    Unit Tests
# '''
# class IncidentReportUnitTests(unittest.TestCase):

#     def test_new_report(self):
#         newReport = IncidentReport(studentID=1, madeByStaffId=2, report="Bad report",topic="Badness", points=-3,studentSeen=False)
#         assert newReport is not None

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

# class IncidentReportIntegrationTests(unittest.TestCase):

#     def test_create_report(self):
#         assert create_student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5") == True
#         assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
#         student = get_student_by_username("billy")
#         staff = get_staff_by_username("joe")

#         assert create_incident_report(student.UniId, staff.ID, "Bad Report", "Badness", points=-3) == True

#     def test_delete_report(self):
#         self.test_create_report()
#         staff = get_staff_by_username("joe")
#         reports = get_incident_reports(staff.ID)
#         report = reports[0]
#         db.session.delete(report)
#         db.session.commit()
#         deleted_report = get_incident_report(report.id)
#         assert deleted_report is None
