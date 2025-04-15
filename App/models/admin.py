from App.database import db
from .user import User


class Admin(User):
  __tablename__ = 'admin'
  ID = db.Column(db.Integer, db.ForeignKey('user.ID', name='fk_admin_user'), primary_key=True)

  __mapper_args__ = {"polymorphic_identity": "admin"}

  def __init__(self, username, firstname, lastname, email, password, faculty):
    super().__init__(username=username,
                     firstname=firstname,
                     lastname=lastname,
                     email=email,
                     password=password,
                     faculty=faculty)


#return admin details on json format

  def to_json(self):
    return {
        "adminID": self.ID,
        "username": self.username,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email,
        "faculty": self.faculty
    }
