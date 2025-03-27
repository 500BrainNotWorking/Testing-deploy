from App.models import Student
from App.database import db


def create_student(username, UniId, firstname, lastname, email, password,
                   faculty, admittedTerm, degree, gpa):
  newStudent = Student(username, UniId, firstname, lastname, email, password,
                       faculty, admittedTerm, degree, gpa)
  db.session.add(newStudent)
  try:
    db.session.commit()
    return True
    # return newStudent
  except Exception as e:
    print(
        "[student.create_student] Error occurred while creating new student: ",
        str(e))
    db.session.rollback()
    return False

def delete_student(uni_id):
  student = get_student_by_UniId(uni_id)
  db.session.delete(student)
  db.session.commit()

def create_student_from_transcript(transcript_data, student_data):
  try:

    #storing UniId, gpa, fullname, faculty, degree, admittedTerm in Student object and linking it to the transcript object
    UniId = transcript_data.get('id')
    gpa = transcript_data.get('gpa')
    faculty = transcript_data.get('faculty')
    admittedTerm = transcript_data.get('admittedTerm')
    #yearOfStudy = transcript_data.get('yearOfStudy')
    degree = transcript_data.get('programme')
    fullname = transcript_data.get('fullname')

    #retrieve student from database and update the student object correctly
    print("Student Data in controller ID is:", student_data.ID)

    #updating student
    #checking if student already exist based on id
    student = get_student_by_id(student_data.ID)
    if not student:
      print(
          f"Student with ID {student.ID} already exists in database from controller!"
      )
      return False
    else:
      #db.session.add(new_student)
      #updating student
      update_from_transcript(student_data.ID, admittedTerm, UniId, gpa, degree,
                             faculty, fullname)
      #db.session.commit()
      #printing data to be stored
      print(
          f"Added row: UniId: {UniId}, GPA: {gpa}, Faculty: {faculty}, Admitted Term: {admittedTerm}, Degree: {degree}, Fullname: {fullname}"
      )
      print("Student data stored in database from controller!")
      return True

  except Exception as e:
    print(
        "[transcript.create_transcript] Error occurred while creating new Student: ",
        str(e))
    db.session.rollback()
    return False


def get_student_by_id(id):
  student = Student.query.filter_by(ID=id).first()
  if student:
    return student
  else:
    return None


def get_student_by_UniId(UniId):
  student = Student.query.filter_by(UniId=UniId).first()
  if student:
    return student
  else:
    return None


def get_student_by_username(username):
  student = Student.query.filter_by(username=username).first()
  if student:
    return student
  else:
    return None


def get_students_by_faculty(faculty):
  students = Student.query.filter_by(faculty=faculty).all()
  if students:
    return students
  else:
    return []

def get_student_review_index(student_id, review_id):
  student = get_student_by_id(student_id)
  return student.get_review_index(review_id)

def get_student_review_id(student_id, review_index):
  student = get_student_by_id(student_id)
  return student.get_review_id(review_index)

def get_student_for_ir(firstname, lastname, UniId):
  student = Student.query.filter_by(firstname=firstname,
                                    lastname=lastname,
                                    UniId=UniId).first()
  if student:
    return student
  else:
    return []


def get_student_by_name(firstname, lastname):
  students = Student.query.filter_by(firstname=firstname,
                                     lastname=lastname).all()
  if students:
    return students
  else:
    return []


def get_full_name_by_student_id(student_id):
  student = Student.query.filter_by(UniId=student_id).first()
  if student:
    full_name = f"{student.firstname} {student.lastname}"
    return full_name
  else:
    return None


def get_students_by_degree(degree):
  students = Student.query.filter_by(degree=degree).all()
  if students:
    return students
  else:
    return []


def get_students_by_ids(student_ids):
  students = Student.query.filter(Student.ID.in_(student_ids)).all()
  return students


# def get_all_students_json():
#   students = Student.query.all()
#   if not students:
#     return []
#   students_json = [student.get_json() for student in students]
#   return students_json


#returning all information about students
def get_all_students_json():
  students = Student.query.all()
  if not students:
    return []

  students_json = []
  for student in students:
    student_data = {
        'id': student.ID,
        'username': student.username,
        'firstname': student.firstname,
        'lastname': student.lastname,
        'email': student.email,
        'faculty': student.faculty,
        #'accomplishments': student.accomplishments,  # Include accomplishments
        #'incidents': student.incidents,  # Include incidents
        'degree': student.degree,  # Include degree
        'admittedTerm': student.admittedTerm,  # Include admitted term
        'gpa': student.gpa,
        #'transcripts': student.transcripts,  # Include transcripts
        #'karmaScore': student.karmaScore,  # Include karma score
        #'karmaRank': student.karmaRank # Include karma rank
        # Include other details as needed
    }
    students_json.append(student_data)

  return students_json


# def student_create_post(studentUsername, teacherUsername, details):
#     if create_post(studentUsername, teacherUsername, verified=False, details):
#         return True
#     else:
#         print("[student.student_create_post] Error occurred while creating new post: create_post returned False")
#         return False


#UniId=UniId, gpa=gpa, firstname=fullname, admittedTerm=admittedTerm, degree=degree, faculty=faculty, username=UniId, lastname="", email="", password=""
def update_from_transcript(ID, newAdmittedTerm, newUniId, newGpa, newDegree,
                           newFaculty, newFullname):
  student = get_student_by_id(ID)
  if student:
    student.admittedTerm = newAdmittedTerm
    student.UniId = newUniId
    student.gpa = newGpa
    student.degree = newDegree
    student.faculty = newFaculty
    #student.fullname = newFullname
    try:
      db.session.commit()
      return True
    except Exception as e:
      print(
          "[student.update_from_transcript] Error occurred while updating student admittedTerm, No student with ID:",
          ID, "was found!", str(e))
      db.session.rollback()
      return False


def update_admittedTerm(studentID, newAdmittedTerm):
  student = get_student_by_id(studentID)
  if student:
    student.admittedTerm = newAdmittedTerm
    try:
      db.session.commit()
      return True
    except Exception as e:
      print(
          "[student.update_admittedTerm] Error occurred while updating student admittedTerm:",
          str(e))
      db.session.rollback()
      return False
  else:
    print(
        "[student.update_admittedTerm] Error occurred while updating student admittedTerm: Student "
        + str(studentID) + " not found")
    return False


# this field doesn't exist in the database for now
def update_yearofStudy(studentID, newYearofStudy):
  student = get_student_by_id(studentID)
  if student:
    student.yearofStudy = newYearofStudy
    try:
      db.session.commit()
      return True
    except Exception as e:
      print(
          "[student.update_yearofStudy] Error occurred while updating student yearofStudy:",
          str(e))
      db.session.rollback()
      return False
  else:
    print(
        "[student.update_yearofStudy] Error occurred while updating student yearofStudy: Student "
        + str(studentID) + " not found")
    return False


def update_degree(studentID, newDegree):
  student = get_student_by_id(studentID)
  if student:
    student.degree = newDegree
    try:
      db.session.commit()
      return True
    except Exception as e:
      print(
          "[student.update_degree] Error occurred while updating student degree:",
          str(e))
      db.session.rollback()
      return False
  else:
    print(
        "[student.update_degree] Error occurred while updating student degree: Student "
        + str(studentID) + " not found")
    return False
