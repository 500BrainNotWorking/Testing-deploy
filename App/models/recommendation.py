from App.database import db
from datetime import datetime


class Recommendation(db.Model):
  __tablename__ = 'recommendation'
  ID = db.Column(db.Integer, primary_key=True)
  createdByStudentID = db.Column(db.String, db.ForeignKey('student.UniId', name='rec_student'))
  taggedStaffID = db.Column(db.Integer, db.ForeignKey('staff.ID', name='rec_staff'))
  studentName = db.Column(db.String(100), nullable=False)
  approved = db.Column(db.Boolean, nullable=False)
  currentYearOfStudy = db.Column(db.String(100), nullable=False)
  details = db.Column(db.String(100), nullable=False)
  dateRequested = db.Column(db.DateTime, default=datetime.utcnow)
  status = db.Column(db.String(100), nullable=False)
  recommendation_type = db.Column(db.String(20), nullable=False)
  studentSeen = db.Column(db.Boolean, nullable=False, default=False)

  __mapper_args__ = {
      "polymorphic_identity": "recommendation",
      "polymorphic_on": recommendation_type
  }

  def __init__(self, student, staffID, approved, status, currentYearOfStudy,
               details, studentSeen):
    self.createdByStudentID = student.UniId
    self.studentName = f"{student.firstname} {student.lastname}"
    self.taggedStaffID = staffID
    self.approved = approved
    self.dateRequested = datetime.now()
    self.status = status
    self.currentYearOfStudy = currentYearOfStudy
    self.details = details
    self.studentSeen = studentSeen

  def get_json(self):
    return {
        'studentID': self.createdByStudentID,
        "name": self.studentName,
        'staffID': self.taggedStaffID,
        'approved': self.approved,
        "date requested": self.dateRequested.strftime("%d-%m-%Y %H:%M"),
        "status": self.status,
        "currentYearOfStudy": self.currentYearOfStudy,
        "details": self.details
    }
