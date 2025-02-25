from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, make_response
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.database import db
from flask_login import login_required, current_user
from sqlalchemy import or_
from datetime import datetime

from App.models import Student, Staff, User, IncidentReport, Comment, Reply
from App.controllers import (
    jwt_authenticate, create_incident_report, get_student_by_UniId,
    get_accomplishment, get_student_by_id, get_recommendations_staff,
    get_recommendation, get_staff_by_id, get_students_by_faculty,
    get_staff_by_id, get_requested_accomplishments, get_transcript,
    get_total_As, get_student_for_ir, create_review, get_karma,
    analyze_sentiment, get_requested_accomplishments_count,
    get_recommendations_staff_count, calculate_ranks, update_total_points,
    calculate_academic_points, calculate_accomplishment_points,
    calculate_review_points, get_all_verified, 
    get_reviews, get_review, 
    create_comment, get_comment, get_comment_staff
    get_reply, create_reply)            #added get_reviews

staff_views = Blueprint('staff_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''

@staff_views.route('/StaffHome', methods=['GET'])
def get_StaffHome_page():

  staff_id = current_user.get_id()
  numAccProp = get_requested_accomplishments_count(staff_id)
  numRRs = get_recommendations_staff_count(staff_id)
  staff=get_staff_by_id(staff_id)

  return render_template('Staff-Home.html',
                         numAccProp=numAccProp,
                         numRRs=numRRs,staff=staff)

@staff_views.route('/staffhome', methods=['GET'])
def get_staffHome_page():

  staff_id = current_user.get_id()
  numAccProp = get_requested_accomplishments_count(staff_id)
  numRRs = get_recommendations_staff_count(staff_id)

  return render_template('Staff-Home.html',
                         numAccProp=numAccProp,
                         numRRs=numRRs)


@staff_views.route('/incidentReport', methods=['GET'])
def staff_ir_page():
  return render_template('IncidentReport.html')


@staff_views.route('/get_student_name', methods=['POST'])
def get_student_name():
  student_id = request.json['studentID']

  student = get_student_by_UniId(student_id)

  return jsonify({'studentName': student.fullname})


@staff_views.route('/studentSearch', methods=['GET'])
def student_search_page():
  return render_template('StudentSearch.html')


@staff_views.route('/reviewSearch', methods=['GET'])
def review_search_page():
  return render_template('ReviewSearch.html')


@staff_views.route('/mainReviewPage', methods=['GET'])
def mainReviewPage():
  return render_template('CreateReview.html')

@staff_views.route('/createReply', methods=['POST'])
@login_required
def createReply():
  staffID = current_user.get_id()
  staff = get_staff_by_id(staff_id) 

  data = request.form #Depening on how the create comment form is made/designed this si subject to change, along with attribute names.

  if staff:
    commentID = data['reviewID']
    details = data['selected-details']

    comment = get_comment(commentID)

    if comment:
      newReply = create_reply(commentID=commentID, staffID=staffID, details=details, parentReplyID=None)
      message = f"You have posted a reply to the Comment: {commentID}" #Keeping review ID in flash message for testign purpose, remove later.
    else:
      message = f"Comment is not found!"
  else:
    message = f"You are not logged in as staff and cannot post a Reply!"


@staff_views.route('/createComment', methods=['POST'])
@login_required
def createComment():
  staffID = current_user.get_id()
  staff = get_staff_by_id(staff_id) 

  data = request.form #Depening on how the create comment form is made/designed this si subject to change, along with attribute names.

  if staff:
    reviewID = data['reviewID']
    details = data['selected-details']

    review = get_review(reviewID)

    if review:
      newComment = create_comment(reviewID=reviewID, staffID=staffID, details=details)
      message = f"You have posted a comment on Review: {reviewID}" #Keeping review ID in flash message for testign purpose, remove later.
    else:
      message = f"Review is not found!"
  else:
    message = f"You are not logged in as staff and cannot post a Comment!"


  return render_template('')#Put the appropriate template here

@staff_views.route('/viewComments/<int:review_id>', methods=['GET'])
@login_required
def view_all_comments(review_id):
  review = get_review(review_id)
  #user = User.query.filter_by(ID=current_user.ID).first()

  comments = get_all_comments()

  return render_template('', comments=comments, review=review)# Put the appropriate template here, and current_user if needed.

@staff_views.route('/editComment/<int:comment_id>', methods=['GET'])
@login_required
def edit_comment(comment_id):
  comment = get_comment(comment_id)
  #user = User.query.filter_by(ID=current_user.ID).first()

  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id) 

  data = request.form #Depening on how the create comment form is made/designed this si subject to change, along with attribute names.

  details = data['selected-details']

  edit_comment(details=details, comment_id=comment_id, staff_id=staff_id)

  return render_template('',current_user=current_user)# Put the appropriate template here, and current_user if needed.

@staff_views.route('/deleteComment/<int:comment_id>', methods=['GET'])
@login_required
def delete_comment(comment_id):
  comment = get_comment(comment_id)
  #user = User.query.filter_by(ID=current_user.ID).first()

  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id) 

  delete_comment(comment_id=comment_id, staff_id=staff_id)

  return render_template('',current_user=current_user)# Put the appropriate template here, and current_user if needed.
  
@staff_views.route('/createReview', methods=['POST'])
@login_required
def createReview():
  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id)

  data = request.form
  studentID = data['studentID']
  studentName = data['name']
  points = int(data['points'])
  print("Start points:", points)
  num = data['num']
  personalReview = data['manual-review']
  details = data['selected-details']
  firstname, lastname = studentName.split(' ')
  student = get_student_by_UniId(studentID)

  if personalReview:
    details += f"{num}. {personalReview}"
    nltk_points = analyze_sentiment(personalReview)
    rounded_nltk_points = round(float(nltk_points))
    points += int(rounded_nltk_points)
    print("Final points:", points)

  if points > 0:
    positive = True
  else:
    positive = False

  if student:
    review = create_review(staff, student, points, details)
    message = f"You have created a review on Student: {studentName}"
    return render_template('Stafflandingpage.html', message=message)
  else:
    message = f"Error creating review on Student: {studentName}"
    return render_template('Stafflandingpage.html', message=message)


@staff_views.route('/newIncidentReport', methods=['POST'])
@login_required
def newIncidentReport():
  data = request.form
  staff_id = current_user.get_id()

  student_id = data['studentID']
  student_name = data['name']
  firstname, lastname = student_name.split(' ')
  student = get_student_for_ir(firstname, lastname, student_id)

  topic = data['topic']
  details = data['details']
  points = data['points-dropdown']

  incidentReport = create_incident_report(student_id, staff_id, details, topic,
                                          points)

  if incidentReport:
    message = f"You have created an incident report on the student {student_name} with a topic of {topic} !"

    return render_template('Stafflandingpage.html', message=message)
  else:
    message = f"Error creating incident report on the student {student_name} with a topic of {topic} !"
    return render_template('Stafflandingpage.html', message=message)


@staff_views.route('/searchStudent', methods=['GET'])
@login_required
def studentSearch():

  name = request.args.get('name')
  studentID = request.args.get('studentID')
  faculty = request.args.get('faculty')
  degree = request.args.get('degree')

  query = Student.query

  if name:
    # Check if the name contains both a first name and a last name
    name_parts = name.split()
    if len(name_parts) > 1:
      # If it contains both first name and last name, filter by full name
      query = query.filter_by(fullname=name)
    else:
      # If it contains only one name, filter by either first name or last name
      query = query.filter(
          or_(Student.firstname.ilike(f'%{name}%'),
              Student.lastname.ilike(f'%{name}%')))

  if studentID:
    query = query.filter_by(UniId=studentID)

  if faculty:
    query = query.filter_by(faculty=faculty)

  if degree:
    query = query.filter_by(degree=degree)

  students = query.all()

  if students:
    return render_template('ssresult.html', students=students)
  else:
    message = "No students found"
    return render_template('StudentSearch.html', message=message)


# @staff_views.route('/review_search/<string:reviewID>', methods=['GET'])
# @login_required
# def reviewSearch(reviewID):

#     if not isinstance(current_user, Staff):
#         return "Unauthorized", 401

#     studentName = request.form.get('student_name')
#     #TOPICS
#     leadership = request.form.get('leadership')
#     respect = request.form.get('respect')
#     punctuality = request.form.get('punctuality')
#     participation = request.form.get('participation')
#     teamwork = request.form.get('teamwork')
#     interpersonal = request.form.get('interpersonal')
#     respect_authority = request.form.get('respect_authority')
#     attendance = request.form.get('attendance')
#     disruption = request.form.get('disruption')

#     # Initialize query with Review model
#     query = Review.query

#     if studentName:
#         query = query.filter_by(studentName=studentName)

#     # Retrieve matching reviews
#     reviews = query.all()

#     if reviews:
#         # Serialize reviews and return as JSON response
#         serialized_reviews = [review.to_json() for review in reviews]
#         return jsonify(serialized_reviews)
#     else:
#         return "No matching records", 404


@staff_views.route('/allAchievementApproval', methods=['GET'])
@login_required
def allAchievementApproval():

  staff_id = current_user.get_id()
  accomplishments = get_requested_accomplishments(staff_id)
  return render_template('ProposedAchievements.html',
                         accomplishments=accomplishments)


@staff_views.route('/approveAchievement/<int:accomplishmentID>',
                   methods=['GET'])
@login_required
def approveAchievement(accomplishmentID):
  accomplishment = get_accomplishment(accomplishmentID)
  student = get_student_by_id(accomplishment.createdByStudentID)

  return render_template('SelectedStudentAccomplishment.html',
                         accomplishment=accomplishment,
                         student=student)


@staff_views.route('/acceptAccomplishment/<int:accomplishmentID>',
                   methods=['POST'])
@login_required
def acceptAccomplishment(accomplishmentID):

  accomplishment = get_accomplishment(accomplishmentID)

  comment = request.form.get('acceptcomment')

  nltk_points = analyze_sentiment(comment)
  rounded_nltk_points = round(float(nltk_points))

  comment = "Accomplishment accepted: " + comment
  accomplishment.points = rounded_nltk_points
  accomplishment.verified = True
  accomplishment.status = comment

  db.session.add(accomplishment)
  db.session.commit()

  message = "You have verified this accomplishment !!"

  return render_template('Stafflandingpage.html', message=message)


@staff_views.route('/declineAccomplishment/<int:accomplishmentID>',
                   methods=['POST'])
@login_required
def declineAccomplishment(accomplishmentID):

  accomplishment = get_accomplishment(accomplishmentID)

  comment = request.form.get('declinecomment')

  nltk_points = analyze_sentiment(comment)
  rounded_nltk_points = round(float(nltk_points))

  comment = "Accomplishment declined: " + comment
  accomplishment.points = rounded_nltk_points
  accomplishment.verified = True
  accomplishment.status = comment

  db.session.add(accomplishment)
  db.session.commit()

  message = "You have declined this accomplishment !!"

  return render_template('Stafflandingpage.html', message=message)


@staff_views.route('/view-all-student-reviews/<string:uniID>', methods=['GET'])
@login_required
def view_all_student_reviews(uniID):

  student = get_student_by_UniId(uniID)
  user = User.query.filter_by(ID=current_user.ID).first()
  return render_template('AllStudentReviews.html', student=student,user=user)


@staff_views.route('/view-all-student-incidents/<string:uniID>',
                   methods=['GET'])
@login_required
def view_all_student_incidents(uniID):

  student = get_student_by_UniId(uniID)
  user = User.query.filter_by(ID=current_user.ID).first()
  return render_template('AllStudentIncidents.html', student=student,user=user)


@staff_views.route('/view-all-student-achievements/<string:uniID>',
                   methods=['GET'])
@login_required
def view_all_student_achievements(uniID):
  student = Student.query.filter_by(UniId=uniID).first()
  user = User.query.filter_by(ID=current_user.ID).first()
  return render_template('AllStudentAchivements.html', student=student,user=user)


# @staff_views.route('/getStudentProfile/<string:uniID>', methods=['GET'])
# @login_required
# def getStudentProfile(uniID):
#   student = Student.query.filter_by(UniId=uniID).first()

#   if student is None:
#     student = Student.query.filter_by(ID=uniID).first()

#   user = User.query.filter_by(ID=student.ID).first()
#   karma = get_karma(student.ID)

#   if karma:

#     calculate_academic_points(student.ID)
#     calculate_accomplishment_points(student.ID)
#     calculate_review_points(student.ID)
#     #Points: academic (0.4),accomplishment (0,3 shared)
#     #missing points: incident , reivew
#     #calculate the accomplishment - incident for 0.3 shared
#     #assign review based on 1 time reivew max 5pts for 0.3
#     update_total_points(karma.karmaID)
#     #updaing ranks
#     calculate_ranks()
#     student.update(karma.rank) #202412 student updates karma rank
#     karma.notify()
#   transcripts = get_transcript(student.UniId)
#   numAs = get_total_As(student.UniId)
#   reviews = get_reviews(student.ID)

#   return render_template('Student-Profile-forStaff.html',
#                          student=student,
#                          user=user,
#                          transcripts=transcripts,
#                          numAs=numAs,
#                          karma=karma,
#                          reviews = reviews)

@staff_views.route('/getStudentProfile/<string:uniID>', methods=['GET'])
@login_required
def getStudentProfile(uniID):
    student = Student.query.filter_by(UniId=uniID).first()

    if student is None:
        student = Student.query.filter_by(ID=uniID).first()

    user = User.query.filter_by(ID=student.ID).first()
    karma = get_karma(student.ID)

    if karma:
        calculate_academic_points(student.ID)
        calculate_accomplishment_points(student.ID)
        calculate_review_points(student.ID)
        update_total_points(karma.karmaID)
        calculate_ranks()
        student.update(karma.rank)
        karma.notify()

    transcripts = get_transcript(student.UniId)
    numAs = get_total_As(student.UniId)
    reviews = get_reviews(student.ID)

    # Attach staff name dynamically
    for review in reviews:
        staff = get_staff_by_id(review.createdByStaffID)  # Get Staff object
        review.staff_name = staff.firstname + " " + staff.lastname if staff else "Unknown Staff"  # Attach fullname

    return render_template('Student-Profile-forStaff.html',
                           student=student,
                           user=user,
                           transcripts=transcripts,
                           numAs=numAs,
                           karma=karma,
                           reviews=reviews)


@staff_views.route('/allRecommendationRequests', methods=['GET'])
@login_required
def allRecommendationRequests():
  staffID = current_user.get_id()
  recommendations = get_recommendations_staff(staffID)
  recommendations_type = type(recommendations)
  print("recommendations type:", recommendations_type)

  return render_template('RecommendationRequests.html',
                         recommendations=recommendations)


@staff_views.route('/declineRR/<int:rrID>', methods=['POST'])
@login_required
def declineRR(rrID):

  recommendation = get_recommendation(rrID)

  recommendation.approved = True
  recommendation.status = "Recommendation Declined"
  db.session.add(recommendation)
  db.session.commit()

  message = "You have declined this recommendation !!"

  return render_template('Stafflandingpage.html', message=message)


@staff_views.route('/acceptRR/<int:rrID>', methods=['POST'])
@login_required
def acceptRR(rrID):
  current_date = datetime.now().strftime("%Y-%m-%d")
  recommendation = get_recommendation(rrID)
  staffID = current_user.get_id()
  staff = get_staff_by_id(staffID)
  student = get_student_by_UniId(recommendation.createdByStudentID)
  # accomplishments = get_all_verified(student.UniId) 
  accomplishments = get_all_verified(student.ID)
  message = "You have accepted this recommendation !!"
  return render_template('RecommendationLetter.html',
                         accomplishments=accomplishments,
                         recommendation=recommendation,
                         current_date=current_date,
                         student=student,
                         staff=staff)

from io import BytesIO
from xhtml2pdf import pisa

@staff_views.route('/makepdf/<int:rrID>', methods=['POST'])
def makePDF(rrID):
    current_date = datetime.now().strftime("%Y-%m-%d")
    recommendation = get_recommendation(rrID)
    staffID = current_user.get_id()
    staff = get_staff_by_id(staffID)
    student = get_student_by_UniId(recommendation.createdByStudentID)

    base64_signature = request.form['signature']
    details = request.form['details']
    html_content = render_template('RecommendationRequestPDF.html',
                                    recommendation=recommendation,
                                    current_date=current_date,
                                    staff=staff,
                                    student=student,
                                    base64_signature=base64_signature,
                                    details=details)
    result = BytesIO()
    pisa.CreatePDF(BytesIO(html_content.encode("utf-8")), result)

    pdf = result.getvalue()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    return response

@staff_views.route('/confirmRL/<int:rrID>', methods=['GET'])
@login_required
def confirmRL(rrID):

  recommendation = get_recommendation(rrID)

  recommendation.approved = True
  recommendation.status = "Recommendation Accepted"
  db.session.add(recommendation)
  db.session.commit()

  message = "You have confirmed this recommendation !!"

  return render_template('Stafflandingpage.html', message=message)

@staff_views.route('/view-all-badges-staff/<string:studentID>', methods=['GET'])
@login_required
def view_all_badges(studentID):
  student = get_student_by_id(studentID)
  user = User.query.filter_by(ID=current_user.ID).first()
  return render_template('AllBadges.html',student=student,user=user)