from App.database import db
from sqlalchemy.sql import func

class Karma(db.Model):

  __tablename__ = "karma"
  karmaID = db.Column(db.Integer, primary_key=True)
  studentID = db.Column(db.Integer, db.ForeignKey('student.ID', use_alter=True))
  reviewID = db.Column(db.Integer, db.ForeignKey('review.ID', use_alter=True))
  points = db.Column(db.Float, nullable=False, default=5.0)
  timestamp = db.Column(db.DateTime, nullable=False, server_default=func.now())

  def __init__(self, points, studentID, reviewID):
    self.points = points
    self.studentID = studentID
    self.reviewID = reviewID

  def to_json(self):
    return {
        "karmaID": self.karmaID,
        "studentID": self.studentID,
        "reviewID": self.reviewID,
        "score": self.points,
        "timestamp": self.timestamp
    }
  
  def __repr__(self):
    return f"Student ID: {self.studentID} Review ID: {self.reviewID} Points: {self.points} Timestamp: {self.timestamp}"