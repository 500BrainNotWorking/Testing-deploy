from App.database import db
from .student import Student

class Grades(db.Model):
  __tablename__ = 'Grades'
  ID = db.Column(db.Integer , primary_key=True)
  studentID = db.Column(db.Integer, db.ForeignKey('student.ID', name='fk_grades_student'))
  course = db.Column(db.String(120), nullable=False)
  grade = db.Column(db.String(120), nullable=False)

  def __init__(self, studentID ,course, grade):
    self.course = course
    self.grade = grade
    self.studentID = studentID

  def to_json(self):
    return {
        "ID": self.ID,
        "studentID": self.studentID,
        "course": self.course,
        "grade": self.grade
    }