from App.database import db
from sqlalchemy.sql import func

class Karma(db.Model):

  __tablename__ = "karma"
  karmaID = db.Column(db.Integer, primary_key=True)
  studentID = db.Column(db.Integer, db.ForeignKey('student.ID', use_alter=True))
  points = db.Column(db.Float, nullable=False, default=0.0)
  timestamp = db.Column(db.DateTime, nullable=False, server_default=func.now())

  def __init__(self, points, studentID):
    self.points = points
    self.studentID = studentID
    
    
  def calculate_total_points(self):
    print("Calculating total points using only review points...")

    # Multiplier for review points
    review_multiplier = 1.0  # Complete weighting of karma depends on reviews, to be altered to include diversity of reviewers

    # Calculation
    print("Review Points:", self.reviewsPoints) 
    print("Review Points Multiplier:", review_multiplier, "giving",
          self.reviewsPoints, "*", review_multiplier, "=", self.reviewsPoints * review_multiplier)

    self.points = round(self.reviewsPoints * review_multiplier, 2)

    # Display the total points calculation
    print("Total Karma Points:", self.points)


  #updates Karma Level
  def updateKarmaLevel(self, rank):
    if (self.rank != rank):
       self.rank = rank
       db.session.add(self)
       db.session.commit()       
       return True
    else:
       return False

  def to_json(self):
    return {
        "karmaID": self.karmaID,
        "studentID": self.studentID,
        "score": self.points,
        "timestamp": self.timestamp
    }
  
  def __repr__(self):
    return f"Student ID: {self.studentID} Points: {self.points} Timestamp: {self.timestamp}"