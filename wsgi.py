import click, pytest, sys
import nltk
from flask import current_app
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.models import Student, Karma, Badges, Accomplishment, Comment
from App.models import User
from App.controllers import (
    create_student, create_staff, create_admin, get_all_users_json,
    get_all_users, get_transcript, get_student_by_UniId, setup_nltk,
    analyze_sentiment, get_total_As, get_total_courses_attempted,
    calculate_academic_score, create_review, create_incident_report,
    create_accomplishment, get_staff_by_id, get_student_by_id,
    create_job_recommendation, create_karma, get_karma, create_badge, 
    calculate_ranks,
    get_accomplishments_by_studentID, get_staff_by_name, create_comment)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
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
    

  #   if student:
  #     print(student.ID)
  #     create_karma(student.ID)
  #     student.karmaID = get_karma(student.ID).karmaID     
  #     print(get_karma(student.ID).karmaID)
  #     db.session.commit()


# @app.cli.command("nltk_test", help="Tests nltk")
# @click.argument("sentence", default="all")
# def analyze(sentence):
#   analyze_sentiment(sentence)
#   return


# '''
# User Commands
# '''

# # Commands can be organized using groups

# # create a group, it would be the first argument of the comand
# # eg : flask user <command>
# # user_cli = AppGroup('user', help='User object commands')

# # # Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(id, username, firstname,lastname , password, email, faculty):
#     create_user(id, username, firstname,lastname , password, email, faculty)
#     print(f'{username} created!')

# # this command will be : flask user create bob bobpass

# @user_cli.command("list", help="Lists users in the database")
# @click.argument("format", default="string")
# def list_user_command(format):
#     if format == 'string':
#         print(get_all_users())
#     else:
#         print(get_all_users_json())

# app.cli.add_command(user_cli) # add the group to the cli
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')

@test.command("unit", help="Run all Unit tests")
def all_tests_command():
    sys.exit(pytest.main(["-k", "UnitTests"]))


@test.command("int", help="Run all Integration tests")
def all_tests_command():
    sys.exit(pytest.main(["-k", "IntegrationTests"]))

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))


@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def student_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StudentUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Student"]))


@test.command("staff", help="Run Staff tests")
@click.argument("type", default="all")
def staff_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StaffUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Staff"]))


@test.command("review", help="Run Review tests")
@click.argument("type", default="all")
def review_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "ReviewIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Review"]))



@test.command("comment", help="Run Comment tests")
@click.argument("type", default="all")
def review_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "CommentUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "CommentIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Comment"]))



@test.command("reply", help="Run Reply tests")
@click.argument("type", default="all")
def review_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ReplyUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "ReplyIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Reply"]))


@test.command("karma", help="Run Karma tests")
@click.argument("type", default="all")
def review_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "KarmaUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "KarmaIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Karma"]))

# @test.command("final", help="Runs ALL tests")
# @click.argument("type", default="all")
# def final_tests_command(type):
#   if type == "all":
#     sys.exit(pytest.main(["App/tests"]))

# @test.command("user", help="Run User tests")
# @click.argument("type", default="all")
# def user_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "UserUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
#   # else:
#   #   sys.exit(pytest.main(["-k", "App"]))


# @test.command("student", help="Run Student tests")
# @click.argument("type", default="all")
# def student_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "StudentUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
#   # else:
#   #   sys.exit(pytest.main(["-k", "App"]))


# @test.command("staff", help="Run Staff tests")
# @click.argument("type", default="all")
# def staff_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "StaffUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
#   # else:
#   #   sys.exit(pytest.main(["-k", "App"]))


# @test.command("review", help="Run Review tests")
# @click.argument("type", default="all")
# def review_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "ReviewIntegrationTests"]))
#   # else:
#   #   sys.exit(pytest.main(["-k", "App"]))


# @test.command("recommendation", help="Run Recommendation tests")
# @click.argument("type", default="all")
# def recommendation_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "RecommendationUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "RecommendationIntegrationTests"]))
#   # else:
#   #   sys.exit(pytest.main(["-k", "App"]))


# @test.command("karma", help="Run Karma tests")
# @click.argument("type", default="all")
# def karma_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "KarmaUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "KarmaIntegrationTests"]))
#   # else:
#   #   sys.exit(pytest.main(["-k", "App"]))


# @test.command("incidentreport", help="Run Incident Report tests")
# @click.argument("type", default="all")
# def incident_reports_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "IncidentReportUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "IncidentReportIntegrationTests"]))
#   # else:
#   #     sys.exit(pytest.main(["-k", "App"]))


# @test.command("accomplishment", help="Run Accomplishment tests")
# @click.argument("type", default="all")
# def accomplishment_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "AccomplishmentUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "AccomplishmentIntegrationTests"]))
#   # else:
#   #     sys.exit(pytest.main(["-k", "App"]))


# @test.command("grades", help="Run Grades tests")
# @click.argument("type", default="all")
# def grades_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "GradesUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "GradesIntegrationTests"]))
#   # else:
#   #     sys.exit(pytest.main(["-k", "App"]))


# @test.command("admin", help="Run Admin tests")
# @click.argument("type", default="all")
# def admin_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "AdminUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "AdminIntegrationTests"]))
#   # else:
#   #     sys.exit(pytest.main(["-k", "App"]))


# @test.command("nltk", help="Run NLTK tests")
# @click.argument("type", default="all")
# def nltk_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "NLTKUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "NLTKIntegrationTests"]))


# @test.command("print", help="print get_transcript")
# @click.argument("type", default="all")
# def print_transcript(type):
#   studentID = input("Enter student ID: ")  # Prompt user to enter student ID
#   transcripts = get_transcript(
#       studentID)  # Get transcript data for the student
#   if transcripts:
#     for transcript in transcripts:
#       if type == "all":
#         print(transcript.to_json())  # Print all transcript data as JSON
#       # elif type == "id":
#       #     print(transcript.studentID)  # Print student ID
#       # elif type == "gpa":
#       #     print(transcript.gpa)  # Print GPA
#       # elif type == "fullname":
#       #     print(transcript.fullname)  # Print full name
#       # Add more options as needed
#       else:
#         print(
#             "Invalid type. Please choose 'all', 'id', 'gpa', 'fullname', or add more options."
#         )
#   else:
#     print("Transcript not found for student with ID:", studentID)


# @test.command("printstu", help="print get_student")
# @click.argument("type", default="all")
# def print_student(type):
#   UniId = input("Enter student ID: ")
#   student = get_student_by_UniId(UniId)
#   if student:
#     if type == "all":
#       print(student.to_json(0))
#     # elif type == "id":
#     #     print(student.UniId)
#     # elif type == "gpa":
#     #     print(student.gpa)
#     # elif type == "fullname":
#     #     print(student.fullname)
#     else:
#       print(
#           "Invalid type. Please choose 'all', 'id', 'gpa', 'fullname', or add more options."
#       )
#   else:
#     print("Student not found with ID:", UniId)


# @test.command("printgradepointsandgpa_weight",
#               help="print student grade points from transcript")
# @click.argument("type", default="all")
# def print_grade_points(type):
#   UniId = input("Enter student ID: ")
#   points = get_total_As(UniId)
#   cources_attempted = get_total_courses_attempted(UniId)
#   if points:
#     print('points ', points)
#     print('courses attepmtped:, ', cources_attempted)

#   else:
#     print("Student not found with ID:", UniId)


# @test.command("printacademicscore", help="print student academic weight")
# @click.argument("type", default="all")
# def print_academic_weight(type):
#   UniId = input("Enter student ID: ")
#   points = get_total_As(UniId)
#   cources_attempted = get_total_courses_attempted(UniId)
#   academic_score = calculate_academic_score(UniId)
#   if points:
#     print('points ', points)
#     print('courses attepmtped:, ', cources_attempted)
#     print('Academic Score:, ', academic_score)

#   else:
#     print("Student not found with ID:", UniId)


app.cli.add_command(test)


# ---- CLI commands ---- #

# 1 add admin user

@app.cli.command('add_admin')
@click.argument('username')
@click.argument('firstname')
@click.argument('lastname')
@click.argument('email')
@click.argument('password')
@click.argument('faculty')
def add_admin(username, firstname, lastname, email, password, faculty):
    
    success = create_admin(username, firstname, lastname, email, password, faculty)
    if success:
        click.echo(f"Admin {username} created successfully!")
    else:
        click.echo(f"Failed to create admin {username}.")
        
        

# 2 search for student (by id, fname, or lname)

@app.cli.command("search_student", help="Search for a student by UniId, first name, or last name")
@click.argument("search_term")
def search_student(search_term):

    students = Student.query.filter(
        (Student.UniId == search_term) |
        (Student.firstname.contains(search_term)) |
        (Student.lastname.contains(search_term))
    ).all()

    if students:
        for student in students:
            print(f"Found student: {student.fullname}, UniId: {student.UniId}")
    else:
        print(f"No student found for search term: {search_term}")


# 3 notify students

@app.cli.command("notify_students", help="Notify students")
@click.argument("message")
def notify_students(message):
    students = Student.query.all()
    for student in students:
        print(f"Notifying {student.fullname} with message: {message}")
    print("Notifications sent to all students.")
    
    
 # 4 update karma points 
 
@app.cli.command("update_karma")
@click.argument("student_id", type=int)
@with_appcontext
def update_karma(student_id):
    print(f"Updating karma for student with ID: {student_id}")
    
    karma = Karma.query.filter_by(studentID=student_id).first()

    if not karma:
        print(f"No karma record found for student with ID: {student_id}. Creating a new one...")
        karma_created = create_karma(student_id)
        if not karma_created:
            print(f"Failed to create karma for student with ID: {student_id}")
            return
    
    if not calculate_review_points(student_id):
        print(f"Failed to update review points for student with ID: {student_id}")
        return

    if not calculate_accomplishment_points(student_id):
        print(f"Failed to update accomplishment points for student with ID: {student_id}")
        return

    if not calculate_incident_points(student_id):
        print(f"Failed to update incident points for student with ID: {student_id}")
        return

    if not calculate_academic_points(student_id):
        print(f"Failed to update academic points for student with ID: {student_id}")
        return

    if not calculate_ranks():
        print("Failed to recalculate ranks for all students.")
        return

    updated_karma = Karma.query.filter_by(studentID=student_id).first()

    if updated_karma:
        print(f"\nUpdated Karma for student ID {student_id}:")
        print(f"Total Karma Points: {updated_karma.points}")
        print(f"Academic Points: {updated_karma.academicPoints}")
        print(f"Accomplishment Points: {updated_karma.accomplishmentPoints}")
        print(f"Review Points: {updated_karma.reviewsPoints}")
        print(f"Incident Points: {updated_karma.incidentPoints}")
        print(f"Rank: {updated_karma.rank}")
    else:
        print(f"Failed to retrieve updated karma for student with ID: {student_id}")
    

# 5 assign badges

@app.cli.command("assign_badge", help="Assign a badge to a student")
@click.argument("UniId", type=int)  
@click.argument("badge_name")
@click.argument("details")
@click.argument("image_link")
@click.argument("student_seen", type=bool)
def assign_badge(UniId, badge_name, details, image_link, student_seen):
    student = get_student_by_UniId(UniId)
    if student:
        badge = Badges(
            student=student,
            name=badge_name,
            details=details,
            imageLink=image_link,
            studentSeen=student_seen
        )
        db.session.add(badge)
        db.session.commit()
        print(f"Badge '{badge_name}' assigned to student {UniId}")
    else:
        print(f"Student with ID {UniId} not found.")
        

# 6 generate leaderboard

@app.cli.command("generate_leaderboard", help="Generate leaderboard of students")
def generate_leaderboard():
    students = Student.query.order_by(Student.gpa.desc()).all() 
    print("Leaderboard:")
    for student in students:
        print(f"{student.fullname} - GPA: {student.gpa}")
        
# 7 manage accomplishments

@app.cli.command("manage_accomplishment", help="Manage student accomplishments")
@click.argument("UniId") 
@click.argument("action", type=click.Choice(['add', 'update', 'delete']))
@click.argument("description")
@click.option('--topic', required=False, help="Topic for the accomplishment (for add/update)")
@click.option('--staff', required=False, help="Staff member's name (for add/update)") 
@click.option('--points', default=0.0, help="Points for the accomplishment (for add/update)")
@click.option('--status', default='pending', help="Status of the accomplishment (for add/update)")
def manage_accomplishment(UniId, action, description, topic, staff, points, status):
    student = get_student_by_UniId(UniId)
    
    if student:
        if action == 'add':
            if not topic or not staff:
                print("Both 'topic' and 'staff' are required for adding an accomplishment.")
                return
            create_accomplishment(student.ID, 
                                  verified=False, 
                                  taggedStaffName=staff, 
                                  topic=topic, 
                                  details=description, 
                                  points=points, 
                                  status=status)
            print(f"Accomplishment added for student {UniId}.")
        
        elif action == 'update':
            accomplishment = get_accomplishments_by_studentID(student.ID)  
            if accomplishment:
                accomplishment.details = description
                if topic:
                    accomplishment.topic = topic
                if staff:
                    firstname, lastname = staff.split(' ')
                    staff_member = get_staff_by_name(firstname, lastname)
                    if staff_member:
                        accomplishment.taggedStaffId = staff_member.ID
                if points:
                    accomplishment.points = points
                if status:
                    accomplishment.status = status
                db.session.commit()
                print(f"Accomplishment updated for student {UniId}.")
            else:
                print(f"No existing accomplishment found for student {UniId}.")

        elif action == 'delete':
            accomplishment = get_accomplishments_by_studentID(student.ID) 
            if accomplishment:
                db.session.delete(accomplishment)
                db.session.commit()
                print(f"Accomplishment deleted for student {UniId}.")
            else:
                print(f"No existing accomplishment found for student {UniId}.")
    else:
        print(f"Student with UniId {UniId} not found.")
        

@app.cli.command("create_karma")
@click.argument("student_id")
@click.argument("points")
def new_karma(student_id, points):
   karma = Karma(points, student_id)
   db.session.add(karma)
   db.session.commit()

@app.cli.command("karma_history")
@click.argument("student_id")
def view_karma_history(student_id):
   student = get_student_by_id(student_id)
   if (student):
      print (student.karma_history)
