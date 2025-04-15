import os
from flask_mailman import Mail
from flask import Flask
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from datetime import timedelta

from App.database import init_db
from App.config import config

from App.controllers import (setup_jwt, setup_flask_login)

from App.views import views




def add_views(app):
  for view in views:
    app.register_blueprint(view)


def configure_app(app, config, overrides):
  for key, value in config.items():
    if key in overrides:
      app.config[key] = overrides[key]
    else:
      app.config[key] = config[key]



def populate_database():

  from App.models import Student, Staff, Review  # or wherever your models live
  from App.controllers import (
      create_student, create_staff, create_admin,
      create_job_recommendation, create_accomplishment,
      create_review, get_staff_by_id, get_student_by_UniId
  )
  from App.database import db

    
  create_student(username="billy",
            firstname="Billy",
            lastname="John",
            email="billy@example.com",
            password="billypass",
            faculty="FST",
            admittedTerm="",
            UniId='816031160',
            degree="",
            gpa="")

  create_student(username="shivum",
                firstname="Shivum",
                lastname="Praboocharan",
                email="shivum.praboocharan@my.uwi.edu",
                password="shivumpass",
                faculty="FST",
                admittedTerm="2019/2021",
                UniId='816016480',
                degree="Bachelor of Computer Science with Management",
                gpa='')

  create_student(username="jovani",
                firstname="Jovani",
                lastname="Highley",
                email="jovani.highley@my.uwi.edu",
                password="jovanipass",
                faculty="FST",
                admittedTerm="2021/2022",
                UniId='816026834',
                degree="Bachelor of Computer Science with Management",
                gpa='')

  create_student(username="kasim",
                firstname="Kasim",
                lastname="Taylor",
                email="kasim.taylor@my.uwi.edu",
                password="kasimpass",
                faculty="FST",
                admittedTerm="2019/2021",
                UniId='816030847',
                degree="Bachelor of Computer Science (General)",
                gpa='')

  create_student(username="brian",
                firstname="Brian",
                lastname="Cheruiyot",
                email="brian.cheruiyot@my.uwi.edu",
                password="brianpass",
                faculty="FST",
                admittedTerm="2021/2022",
                UniId='816031609',
                degree="Bachelor of Computer Science (General)",
                gpa="")

  #Creating staff
  create_staff(username="tim",
              firstname="Tim",
              lastname="Long",
              email="",
              password="timpass",
              faculty="")

  create_staff(username="vijay",
              firstname="Vijayanandh",
              lastname="Rajamanickam",
              email="Vijayanandh.Rajamanickam@sta.uwi.edu",
              password="vijaypass",
              faculty="FST")

  create_staff(username="permanand",
              firstname="Permanand",
              lastname="Mohan",
              email="Permanand.Mohan@sta.uwi.edu",
              password="password",
              faculty="FST")

  create_job_recommendation(
      2, 7, False, "Job", "1",
      "I am seeking a recommnedation for a position at a company", "WebTech",
      "Web Developer", "webtech@gmail.com")
  create_job_recommendation(
      2, 8, False, "Job", "1",
      "I am seeking a recommnedation for a position at a company", "WebTech",
      "Web Developer", "webtech@gmail.com")
  create_accomplishment(2, False, "Permanand Mohan", "Runtime",
                        "I placed first at runtime.", 1, "None Yet")
  create_accomplishment(2, False, "Vijayanandh Rajamanickam", "Runtime",
                        "I placed first at runtime.", 1, "None Yet")


  staff = get_staff_by_id(7)
  student1 = get_student_by_UniId('816031609')
  review1 = create_review(staff, student1, 5, "Behaves very well in class!")
  create_review(staff, student1, 2, "Late to class")
  create_review(staff, student1, 5, "Good CW grades")
  create_review(staff, student1, 3, "Okay Final grades")

  student2 = get_student_by_UniId('816016480')
  create_review(staff, student2, 5, "Behaves very well in class!")
  student3 = get_student_by_UniId('816026834')
  create_review(staff, student3, 3, "Behaves very well in class!")
  student4 = get_student_by_UniId('816030847')
  create_review(staff, student4, 5, "Behaves very well in class!")
  create_admin(username="admin",
              firstname="Admin",
              lastname="Admin",
              email="admin@example.com",
              password="password",
              faculty="FST")
  db.session.commit()
      


def create_app(config_overrides={}):
  app = Flask(__name__, static_url_path='/static')
  configure_app(app, config, config_overrides)
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.config['SEVER_NAME'] = '0.0.0.0'
  app.config['PREFERRED_URL_SCHEME'] = 'https'
  app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
  app.config['UPLOAD_FOLDER'] = 'uploads'
  app.config['MAIL_SERVER'] = "smtp.googlemail.com"
  app.config['MAIL_PORT'] = 587
  app.config['MAIL_USE_TLS'] = True
  app.config['MAIL_USE_SSL'] = False
  app.config['MAIL_USERNAME'] = "ttstudentconduct@gmail.com"
  app.config['MAIL_PASSWORD'] = "uvxa guap twon mzwa"
  app.config['MAIL_DEFAULT_SENDER'] = 'ttstudentconduct@gmail.com'
  CORS(app)
  photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
  configure_uploads(app, photos)
  add_views(app)
  init_db(app)
  setup_jwt(app)
  setup_flask_login(app)
  mail = Mail(app)
  app.app_context().push()

  @app.before_first_request
  def before_first_request_func():
    from App.models import Student, Staff, Review  # or wherever your models live
    from App.controllers import (
        create_student, create_staff, create_admin,
        create_job_recommendation, create_accomplishment,
        create_review, get_staff_by_id, get_student_by_UniId
    )
    from App.database import db
    if not Student.query.first() and not Staff.query.first() and not Review.query.first():
      populate_database()

  return app
