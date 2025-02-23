from App.database import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comment'
    ID = db.Column(db.Integer, primary_key=True)
    reviewID = db.Column(db.Integer, db.ForeignKey('review.ID'), nullable = False)
    createdByStaffID = db.Column(db.Integer, db.ForeignKey('staff.ID'), nullable = False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.String(400), nullable=False)

    replies = db.relationship('Reply', backref='comment', lazy=True)
    
    def __init__(self, reviewID, staffID, details):
        self.createdByStaffID = staffID
        self.reviewID = reviewID
        self.details = details
        self.dateCreated = datetime.now()
    
    def get_id(self):
        return self.ID
