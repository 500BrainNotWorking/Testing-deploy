from App.database import db
from .recommendation import Recommendation


class JobRecommendation(Recommendation):
  __tablename__ = 'jobRecommendation'
  ID = db.Column(db.Integer,
                 db.ForeignKey('recommendation.ID', name='fk_jobrec_id'),
                 primary_key=True)
  company = db.Column(db.String(100), nullable=False)
  position = db.Column(db.String(100), nullable=False)
  companyEmail = db.Column(db.String(100), nullable=False)

  __mapper_args__ = {"polymorphic_identity": "jobRecommendation"}

  def __init__(self, currentYearOfStudy, details, student, staffID, approved,
               status, company, position, companyEmail):
    super().__init__(student=student,
                     staffID=staffID,
                     approved=approved,
                     status=status,
                     currentYearOfStudy=currentYearOfStudy,
                     details=details,
                     studentSeen=False)
    self.company = company
    self.position = position
    self.companyEmail = companyEmail

  def __repr__(self):
    return f'<JobRecommendation {self.ID} >'
