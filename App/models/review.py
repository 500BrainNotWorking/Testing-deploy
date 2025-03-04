from App.database import db
from .student import Student
from .karma import Karma  # Import Karma model
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'
    ID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.ID'))
    createdByStaffID = db.Column(db.Integer, db.ForeignKey('staff.ID'))
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    starRating = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String(400), nullable=False)
    comments = db.relationship('Comment', backref='review', lazy=True)

    def __init__(self, staff, student, starRating, details):
        self.createdByStaffID = staff.ID
        self.studentID = student.ID
        self.starRating = starRating
        self.details = details
        self.dateCreated = datetime.now()
        self.adjustKarma()  # Call adjustKarma when a review is created

    def get_id(self):
        return self.ID

    def to_json(self):
        return {
            "reviewID": self.ID,
            "studentID": self.studentID,
            "createdByStaffID": self.createdByStaffID,
            "dateCreated": self.dateCreated.strftime("%d-%m-%Y %H:%M"),  # Format the date/time
            "starRating": self.starRating,
            "details": self.details
        }

    def adjustKarma(self):
        """Adjust the student's karma based on the star rating of the review."""
        if self.starRating == 5:
            points = 5
        elif self.starRating == 4:
            points = 3
        elif self.starRating == 3:
            points = 1
        elif self.starRating == 2:
            points = -1
        else:
            points = -3

        # Fetch the student's latest karma entry
        student = Student.query.get(self.studentID)
        if not student:
            return  # No student found, exit

        latest_karma = student.get_karma()

        if latest_karma:
            # Update existing karma
            latest_karma.points += points
        else:
            # Create new karma record if none exists
            new_karma = Karma(points=points, studentID=self.studentID)
            db.session.add(new_karma)

        db.session.commit()  # Save changes

