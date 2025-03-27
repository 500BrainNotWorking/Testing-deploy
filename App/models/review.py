from App.database import db
from .student import Student
from .karma import Karma  # Import Karma model
from datetime import datetime
from sqlalchemy import func

class Review(db.Model):
    __tablename__ = 'review'
    ID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.ID'))
    createdByStaffID = db.Column(db.Integer, db.ForeignKey('staff.ID'))
    dateCreated = db.Column(db.DateTime, server_default=func.now())
    starRating = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String(400), nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)
    comments = db.relationship('Comment', backref='review', lazy=True)

    liked_by_staff = db.Column(db.String, default='')
    disliked_by_staff = db.Column(db.String, default='')

    def __init__(self, staff, student, starRating, details):
        self.createdByStaffID = staff.ID
        self.studentID = student.ID
        self.starRating = starRating
        self.details = details

    def get_id(self):
        return self.ID

    def to_json(self):
        return {
            "reviewID": self.ID,
            "studentID": self.studentID,
            "createdByStaffID": self.createdByStaffID,
            "dateCreated": self.dateCreated.strftime("%d-%m-%Y %H:%M"),  # Format the date/time
            "starRating": self.starRating,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "details": self.details
        }