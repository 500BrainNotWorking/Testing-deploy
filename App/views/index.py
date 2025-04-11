from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db, Student, Karma
from App.controllers import (
    create_user,
    create_student,
    create_staff,
    create_admin,
    create_karma,
    create_job_recommendation,
    create_accomplishment,
    get_staff_by_id,
    get_student_by_UniId,
    create_review,
)
from flask_login import login_required, login_user, current_user, logout_user

index_views = Blueprint('index_views',
                        __name__,
                        template_folder='../templates')


@index_views.route('/', methods=['GET'])
def index_page():
  return render_template('login.html')


@index_views.route('/hello')
def hello_world():
  return 'Hello, World!'


@index_views.route('/admin', methods=['GET'])
@login_required
def admin_page():
  return render_template('Admin-Home.html')


@index_views.route('/studentcsv', methods=['GET'])
def indexs_page():
  return render_template('StudentCSV.html')


@index_views.route('/staffcsv', methods=['GET'])
def csvStaffPage():
  return render_template('StaffCSV.html')


@index_views.route('/init', methods=['GET'])
def init():
  db.drop_all()
  db.create_all()

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
  student1 = get_student_by_UniId(816031609)
  review1 = create_review(staff, student1, 5, "Behaves very well in class!")
  create_review(staff, student1, 2, "Late to class")
  create_review(staff, student1, 5, "Good CW grades")
  create_review(staff, student1, 3, "Okay Final grades")

  student2 = get_student_by_UniId(816016480)
  create_review(staff, student2, 5, "Behaves very well in class!")
  student3 = get_student_by_UniId(816026834)
  create_review(staff, student3, 3, "Behaves very well in class!")
  student4 = get_student_by_UniId(816030847)
  create_review(staff, student4, 5, "Behaves very well in class!")
  create_admin(username="admin",
               firstname="Admin",
               lastname="Admin",
               email="admin@example.com",
               password="password",
               faculty="FST")

  students = Student.query.all()

  # for student in students:
  #   create_karma(student.ID)
  #   student.karmaID = Karma.query.filter_by(
  #       studentID=student.ID).first().karmaID

  return jsonify(message='db initialized!')


@index_views.route('/health', methods=['GET'])
def health_check():
  return jsonify({'status': 'healthy'})


@index_views.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
  return send_from_directory('/workspaces/Info3604_Project/images', filename)
