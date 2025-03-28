from App.models import Karma, Student
from App.database import db
from .accomplishment import (get_total_accomplishment_points)
from .incidentReport import (get_total_incident_points)
from .transcript import (calculate_academic_score)


def get_karma(studentID):
  karma = Karma.query.filter_by(studentID=studentID).order_by(Karma.timestamp.desc()).first()
  if karma:
    return karma
  else:
    return None


def get_karma_history(studentID):
  history = Karma.query.filter_by(studentID = studentID).order_by(Karma.timestamp.desc())
  if history:                                                                                  #FOR GRAPH, IF BREAK ITS HERE
    return history
  else:
    return None

def get_karma_student(student):
  karma = Karma.query.filter_by(studentID=student.ID).order_by(Karma.timestamp.desc()).first()
  if karma:
    return karma
  else:
    return None

def create_karma(studentID, points, reviewID):
  newKarma = Karma(points=points, studentID=studentID, reviewID=reviewID)
  db.session.add(newKarma)
  try:
    db.session.commit()
    return True
  except Exception as e:
    print("[karma.create_karma] Error occurred while creating new karma: ", str(e))
    return False

def calculate_ranks():
    students = Student.query.all()

    # Create a list of (karma points, student ID)
    student_karma = [
        (student.get_karma().points if student.get_karma() else 0, student.ID)
        for student in students
    ]

    # Sort by karma points in descending order
    student_karma.sort(reverse=True, key=lambda x: x[0])

    # Assign ranks
    for rank, (karma, student_id) in enumerate(student_karma, start=1):
        student = Student.query.get(student_id)
        student.update(rank)  # 
          # 



