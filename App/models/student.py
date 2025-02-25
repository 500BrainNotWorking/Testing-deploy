from App.database import db
from .user import User
from .studentInterface import StudentInterface
from .karma import Karma

class Student(User, StudentInterface):
  __tablename__ = 'student'
  ID = db.Column(db.Integer, db.ForeignKey('user.ID'), primary_key=True)
  UniId = db.Column(db.String(10), nullable=False)
  degree = db.Column(db.String(120), nullable=False)
  fullname = db.Column(db.String(255), nullable=True)
  degree = db.Column(db.String(120), nullable=False)
  admittedTerm = db.Column(db.String(120), nullable=False)
  #yearOfStudy = db.Column(db.Integer, nullable=False)
  gpa = db.Column(db.String(120), nullable=True)

  reviews = db.relationship('Review', backref='studentReviews', lazy='joined')
  accomplishments = db.relationship('Accomplishment',
                                    backref='studentAccomplishments',
                                    lazy='joined')
  incidents = db.relationship('IncidentReport',
                              backref='studentincidents',
                              lazy='joined')
  grades = db.relationship('Grades', backref='studentGrades', lazy='joined')
  transcripts = db.relationship('Transcript', backref='student', lazy='joined')
  badges = db.relationship('Badges', backref='studentbadge', lazy='joined')
  karma_history = db.relationship('Karma')

  __mapper_args__ = {"polymorphic_identity": "student"}

  def __init__(self, username, UniId, firstname, lastname, email, password,
               faculty, admittedTerm, degree, gpa):

    super().__init__(username=username,
                     firstname=firstname,
                     lastname=lastname,
                     email=email,
                     password=password,
                     faculty=faculty)
    self.admittedTerm = admittedTerm
    #self.yearOfStudy = yearofStudy
    self.UniId = UniId
    self.degree = degree
    self.gpa = gpa
    self.reviews = []
    self.fullname = firstname + ' ' + lastname
    self.accomplishments = []
    self.incidents = []
    self.grades = []
    self.transcripts = []
    self.badges = []

  def get_id(self):
    return self.ID

  # Gets the student details and returns in JSON format
  def to_json(self, karma):

    return {
        "studentID":
        self.ID,
        "username":
        self.username,
        "firstname":
        self.firstname,
        "lastname":
        self.lastname,
        "gpa":
        self.gpa,
        "email":
        self.email,
        "faculty":
        self.faculty,
        "degree":
        self.degree,
        "admittedTerm":
        self.admittedTerm,
        #   "yearOfStudy": self.yearOfStudy,
        "UniId":
        self.UniId,
        # "reviews": [review.to_json() for review in self.reviews],
        "accomplishments":
        [accomplishment.to_json() for accomplishment in self.accomplishments],
        "incidents": [incident.to_json() for incident in self.incidents],
        "grades": [grade.to_json() for grade in self.grades],
        "transcripts":
        [transcript.to_json() for transcript in self.transcripts],
        "karma_history" : [karma.to_json() for karma in self.karma_history]
    }

  def get_karma(self):
      if (len(list(self.karma_history)) != 0):
        return self.karma_history[-1]

  def update(self, rank):
      """Update the karma rank for the student"""
      karma = self.get_karma()
      return karma.updateKarmaLevel(rank)
      
