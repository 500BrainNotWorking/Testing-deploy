from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from App.database import db
from .index import index_views
from App.models import Staff, Student, User
from App.controllers import (
    create_user, get_recommendations_student, login, get_transcript,
    get_student_by_UniId, get_recommendations_student_count,
    create_accomplishment, get_all_students_json, get_total_As, get_karma,
    calculate_academic_points, calculate_accomplishment_points,
    get_staff_by_name, calculate_ranks, calculate_review_points,
    create_job_recommendation, create_school_recommendation,
    update_total_points, calculate_incident_points, sortBadges)

student_views = Blueprint('student_views',
                          __name__,
                          template_folder='../templates')
'''
Page/Action Routes
'''

@student_views.route('/StudentHome', methods=['GET'])
@login_required
def student_home_page():
  student = Student.query.filter_by(ID=current_user.ID).first()

  #notis for incidents
  incidentsUnseenNum = 0
  if student:
    for incident in student.incidents:
      if incident.studentSeen == False:
        incidentsUnseenNum += 1

  #notis for accomplishments
  studentVerifiedSeenNum = 0
  if student:
    for achievement in student.accomplishments:
      if achievement.studentSeen == False and achievement.verified == True:
        studentVerifiedSeenNum += 1

  #notis for reviews
  studentReviewsdSeenNum = 0
  if student:
    for review in student.reviews:
      if review.studentSeen == False:
        studentReviewsdSeenNum += 1

  sortBadges(student)

  #notis for badges
  studentBadgesSeenNum = 0
  if student:
    for badge in student.badges:
      if badge.studentSeen == False:
        studentBadgesSeenNum += 1

  recCount = get_recommendations_student_count(current_user.UniId)
  totalNotis = incidentsUnseenNum + studentVerifiedSeenNum + studentReviewsdSeenNum + recCount + studentBadgesSeenNum
  return render_template('Student-Home.html', student=student,totalNotis=totalNotis)

@student_views.route('/Student-Home', methods=['GET'])
@login_required
def home_page():
  student = Student.query.filter_by(ID=current_user.ID).first()

  #notis for incidents
  incidentsUnseenNum = 0
  if student:
    for incident in student.incidents:
      if incident.studentSeen == False:
        incidentsUnseenNum += 1

  #notis for accomplishments
  studentVerifiedSeenNum = 0
  if student:
    for achievement in student.accomplishments:
      if achievement.studentSeen == False and achievement.verified == True:
        studentVerifiedSeenNum += 1

  #notis for reviews
  studentReviewsdSeenNum = 0
  if student:
    for review in student.reviews:
      if review.studentSeen == False:
        studentReviewsdSeenNum += 1

  sortBadges(student)

  #notis for badges
  studentBadgesSeenNum = 0
  if student:
    for badge in student.badges:
      if badge.studentSeen == False:
        studentBadgesSeenNum += 1

  recCount = get_recommendations_student_count(current_user.UniId)
  totalNotis = incidentsUnseenNum + studentVerifiedSeenNum + studentReviewsdSeenNum + recCount + studentBadgesSeenNum
  return render_template('Student-Home.html',totalNotis=totalNotis)


@student_views.route('/student_dashboard', methods=['GET'])
@login_required
def student_dashboard_page():
  return render_template('StudentPage.html')


@student_views.route('/student-page', methods=['GET'])
@login_required
def student_page():
  #getting student info from controller
  #using flasklogin to get the current user
  student = Student.query.filter_by(ID=current_user.ID).first()
  user = User.query.filter_by(ID=current_user.ID).first()
  karma = get_karma(student.ID)
  if karma:
    #print("karma id is: ", karma.karmaID)
    calculate_academic_points(student.ID)
    calculate_accomplishment_points(student.ID)
    calculate_review_points(student.ID)
    calculate_incident_points(student.ID)
    print("academic points:" + str(karma.academicPoints))
    print("accomplishment points:" + str(karma.accomplishmentPoints))
    print("review points:" + str(karma.reviewsPoints))
    print("incident points:" + str(karma.incidentPoints))
    #Points: academic (0.4),accomplishment (0,3 shared)
    update_total_points(student.ID)
    print('total karma points', karma.reviewsPoints)
    #updaing ranks
    calculate_ranks()
    #print(karma.to_json())

  transcripts = get_transcript(current_user.UniId)
  numAs = get_total_As(current_user.UniId)

  sortBadges(student) 
  #notis for incidents
  incidentsUnseenNum = 0
  if student:
    for incident in student.incidents:
      if incident.studentSeen == False:
        incidentsUnseenNum += 1

  #notis for accomplishments
  studentAchieiveSeenNum = 0
  if student:
    for achievement in student.accomplishments:
      if achievement.studentSeen == False and achievement.verified == True:
        studentAchieiveSeenNum += 1

  #notis for reviews
  studentReviewsdSeenNum = 0
  if student:
    for review in student.reviews:
      if review.studentSeen == False:
        studentReviewsdSeenNum += 1

  #notis for badges
  studentBadgesSeenNum = 0
  if student:
    for badge in student.badges:
      if badge.studentSeen == False:
        studentBadgesSeenNum += 1

  recCount = get_recommendations_student_count(current_user.UniId)

  notification_values = [
      incidentsUnseenNum, studentAchieiveSeenNum, studentReviewsdSeenNum,
      recCount ,studentBadgesSeenNum
  ] 
  if student:
    return render_template('StudentPage.html',
                           student=student,
                           user=user,
                           transcripts=transcripts,
                           numAs=numAs,
                           karma=karma,
                           notification_values=notification_values)
  else:
    return render_template('Student-Home.html')


@student_views.route('/api/student-page', methods=['GET'])
@jwt_required()
#@jwt_or_login_required()
def student_page_api():
  # Getting student info from controller
  # Using Flask-Login to get the current user
  student = Student.query.filter_by(ID=jwt_current_user.ID).first()
  user = User.query.filter_by(ID=jwt_current_user.ID).first()
  karma = get_karma(student.ID)

  if karma:
    calculate_academic_points(student.ID)
    calculate_accomplishment_points(student.ID)
    karma.calculate_total_points()

  transcripts = get_transcript(jwt_current_user.UniId)
  numAs = get_total_As(jwt_current_user.UniId)

  #todo calculat rank of student

  if student:
    # Student data found
    return jsonify({
        'student':
        student.to_json(karma),
        'transcripts': [transcript.to_json()
                        for transcript in transcripts] if transcripts else [],
        'numAs':
        numAs if numAs is not None else 0,
        'karma':
        karma.to_json() if karma else None
    })
  else:
    # No student data found
    return jsonify({'error': 'Student data not found'}), 404


@student_views.route('/upload-transcript', methods=['GET'])
@login_required
def student_profile():
  return render_template('uploadtranscript.html')


@student_views.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
  return send_from_directory('/workspaces/Info3604_Project/images', filename)


#route for request recommendation
@student_views.route('/request-recommendation-form', methods=['GET'])
@login_required
def recommendation():

  staff_members = Staff.query.all()

  staff_names = [(staff.firstname, staff.lastname) for staff in staff_members]
  return render_template('request recommendation.html',
                         staff_names=staff_names)


#route for viewing achievements
@student_views.route('/view-achievements', methods=['GET'])
@login_required
def view_achievements():
  return render_template('view-achievements.html')


@student_views.route('/api/view-all-achievements', methods=['GET'])
@jwt_required()
def view_all_achievements_api():
  # Return the students' details in JSON format
  student = get_student_by_UniId(jwt_current_user.UniId)

  # Check if the student exists
  if student:
    achievements = []
    for achievement in student.accomplishments:
      achievement_data = {
          'id': achievement.id,
          'createdByStudentID': achievement.createdByStudentID,
          'taggedStaffId': achievement.taggedStaffId,
          'points': achievement.points,
          'report': achievement.details,
      }
      achievements.append(achievement_data)

    return jsonify({'achievement': achievements}), 200
  else:
    return jsonify({'message': 'Student not found'}), 404


#route for viewing Incidents
@student_views.route('/view-incidents', methods=['GET'])
@login_required
def view_incidents():
  return render_template('View-incidents.html')


@student_views.route('/propose-achievement', methods=['GET'])
@login_required
def propose_achievement():
  staff_members = Staff.query.all()

  # Extract first name and last name fields from each staff member
  staff_names = [(staff.firstname, staff.lastname) for staff in staff_members]
  return render_template('StudentProposeAchievement.html',
                         staff_names=staff_names)


@student_views.route('/request-recommendation', methods=['POST'])
@login_required
def request_recommendation():
  # Extract data from the request
  student_id = current_user.get_id()
  teacherName = request.form.get('taggedStaffName')
  firstname, lastname = teacherName.split(' ')
  staff = get_staff_by_name(firstname, lastname)
  cyos = request.form.get('cyos')
  approved = False

  recommendation_type = request.form.get('recommendationType')

  if recommendation_type == 'Job':
    company_name = request.form.get('companyName')
    position = request.form.get('position')
    company_email = request.form.get('companyEmail')
    details = request.form.get('jobdetails')
    status = "Recommendation Submitted - Pending Approval"
    # Handle job recommendation
    newrec = create_job_recommendation(student_id, staff.ID, approved, status,
                                       cyos, details, company_name, position,
                                       company_email)
    message = f"You have submitted a {recommendation_type} recommendation request to {teacherName}!!"

    return render_template('landingpage.html', message=message)
  elif recommendation_type == 'School':
    school_name = request.form.get('schoolName')
    program = request.form.get('program')
    school_email = request.form.get('schoolEmail')
    details = request.form.get('schooldetails')
    status = "Recommendation Submitted - Pending Approval"
    # Handle job recommendation
    newrec = create_school_recommendation(student_id, staff.ID, approved,
                                          status, cyos, details, school_name,
                                          program, school_email)
    message = f"You have submitted a {recommendation_type} recommendation request to {teacherName}!!"

    return render_template('landingpage.html', message=message)
  return "Request for recommendation submitted successfully!"



@student_views.route('/api/request-recommendation', methods=['POST'])
@jwt_required()
def request_recommendation_api():
  # Extract data from the request
  student_id = jwt_current_user.get_id()
  teacherName = request.form.get('taggedStaffName')
  firstname, lastname = teacherName.split(' ')
  staff = get_staff_by_name(firstname, lastname)
  cyos = request.form.get('cyos')
  approved = False

  recommendation_type = request.form.get('recommendationType')

  if recommendation_type == 'Job':
    company_name = request.form.get('companyName')
    position = request.form.get('position')
    company_email = request.form.get('companyEmail')
    details = request.form.get('jobdetails')
    status = "Job"
    # Handle job recommendation
    newrec = create_job_recommendation(student_id, staff.ID, approved, status,
                                       cyos, details, company_name, position,
                                       company_email)
    message = f"You have submitted a {recommendation_type}  recommendation request to {teacherName}!!"

  elif recommendation_type == 'School':
    school_name = request.form.get('schoolName')
    program = request.form.get('program')
    school_email = request.form.get('schoolEmail')
    details = request.form.get('schooldetails')
    status = "School"
    # Handle school recommendation
    newrec = create_school_recommendation(student_id, staff.ID, approved,
                                          status, cyos, details, school_name,
                                          program, school_email)
    message = f"You have submitted a recommendation request to {teacherName} {details}!!"

  # Construct the JSON response
  response_data = {"message": message}

  # Return the JSON response
  return jsonify(response_data)


@student_views.route('/api/propose-achievement', methods=['POST'])
@login_required
def propose_achievement_post():
  if request.method == 'POST':
    # Extract data from the request
    topic = request.form.get('topic')
    taggedStaffName = request.form.get('taggedStaffName')
    details = request.form.get('details')
    student_id = current_user.ID
    print(student_id)
    print(topic)
    print(taggedStaffName)
    status = "None yet"

    # Check if any required field is missing
    if not all([student_id, taggedStaffName, details]):
      return jsonify({'message': 'All fields are required.'}), 400

    # Call the controller function
    try:
      response = create_accomplishment(student_id, False, taggedStaffName,
                                       topic, details, 0, status)
      message = f"You have submitted an achievement to be verified by {taggedStaffName} !!"

      return render_template('landingpage.html', message=message)
    except Exception as e:
      return jsonify({'message': str(e)}), 500
  else:
    return jsonify({'message': 'Method not allowed'}), 405


@student_views.route('/api/jwtpropose-achievement', methods=['POST'])
#@jwt_or_login_required()
@jwt_required()
def propose_achievement_post_jwt():
  if request.method == 'POST':
    # Extract data from the request
    topic = request.form.get('topic')
    tagged_staff_name = request.form.get(
        'taggedStaffName'
    )  # todo get id from name displayed in list in front end
    details = request.form.get('details')
    student_id = jwt_current_user.ID

    # Check if any required field is missing
    if not all([student_id, tagged_staff_name, details]):
      return jsonify({'message': 'All fields are required.'}), 400

    # Call the controller function
    try:
      response = create_accomplishment(student_id, False, tagged_staff_name,
                                       topic, details, 0, "None yet")
      if response:
        message = f"You have submitted {topic} achievement to be verified by {tagged_staff_name} !!"

        # Return a JSON response with success message
        return jsonify({'message': message}), 200
    except Exception as e:
      # Return a JSON response with error message
      return jsonify({'message': str(e)}), 500
  else:
    # Return a JSON response for method not allowed
    return jsonify({'message': 'Method not allowed'}), 405
  return jsonify(
      {'message': 'Failed to submit achievement, check teachername'}), 405


@student_views.route('/leaderboard', methods=['GET'])
@login_required
def leaderboard_api():
    # Retrieve all students
    students = Student.query.all()

    # Ensure students exist before proceeding
    if not students:
        return render_template('Leaderboard.html', students_json=[])

    # Recalculate karma points (ignoring rank)
    calculate_ranks()

    # Convert to JSON and get karma scores
    students_json = [
        stu.to_json(stu.get_karma()) for stu in students
    ]

    # Sort students by karma score (descending order)
    sorted_students = sorted(students, key=lambda s: s.get_karma().points if s.get_karma() else 0, reverse=True)

    # Generate ranks dynamically (1-based index)
    ranks = list(range(1, len(sorted_students) + 1))

    # Zip students and ranks together
    students_with_ranks = list(zip(sorted_students, ranks))

    # Pass it to the template
    return render_template(
        'Leaderboard.html',
        students_with_ranks=students_with_ranks
    )







# @student_views.route('/api/leaderboard', methods=['GET'])
# @jwt_required()
# def jwt_leaderboard_api():
#   # Getting students' details from controller
#   students = get_all_students_json()
#   students = Student.query.all()

#   #Recalculating points for each student and ranks
#   for student in students:
#     karma = get_karma(student.ID)
#     if karma:

#       calculate_academic_points(student.ID)
#       calculate_accomplishment_points(student.ID)
#       calculate_review_points(student.ID)
#       calculate_incident_points(student.ID)
#       print("review points:" + str(karma.reviewsPoints))
#       #Points: academic (0.4),accomplishment (0,3 shared)
#       #missing points: incident , reivew
#       #calculate the accomplishment - incident for 0.3 shared
#       #assign review based on 1 time reivew max 5pts for 0.3
#       update_total_points(karma.karmaID)
#       print('total karma points', karma.points)
#       print(karma.to_json())

#   students_json = []  # Initialize students_json list

#   # Return the students' details in JSON format
#   calculate_ranks()
#   for stu in students:
#     print('gathering students and their karma info using student json')
#     student_info = stu.to_json(get_karma(stu.ID))
#     students_json.append(
#         student_info)  # Append each student's info to the students_json list
#     print(students_json)

#   # Traverse students, invoke calculate ranking for all
#   # Order object based on ranking
#   sorted_students = sorted(students_json, key=lambda x: x['karmaRank'])
#   sorted_students_json = []

#   for student in sorted_students:
#     sorted_students_json.append({
#         'name': student['username'],
#         'score': student['karmaScore'],
#         'rank': student['karmaRank']
#     })
#   return (sorted_students_json)
#   #return jsonify({'students': students_data}), 200


@student_views.route('/view-all-reviews', methods=['GET'])
@login_required
def view_all_reviews():
  student = get_student_by_UniId(current_user.UniId)
  user = User.query.filter_by(ID=current_user.ID).first()
  if student:
    for review in student.reviews:
      review.studentSeen = True
      print(review.studentSeen)
      db.session.add(review)
      db.session.commit()
  return render_template('AllStudentReviews.html', student=student ,user=user)
  #return jsonify({'students': students_data}), 20
0

@student_views.route('/view-all-badges', methods=['GET'])
@login_required
def view_all_badges():
  user = User.query.filter_by(ID=current_user.ID).first()
  student = get_student_by_UniId(current_user.UniId)

  if student:
    for badge in student.badges:
      badge.studentSeen = True
      db.session.add(badge)
      db.session.commit()
  return render_template('AllBadges.html' ,student=student ,user=user
)

@student_views.route('/api/view-all-reviews', methods=['GET'])
@jwt_required()
def view_all_reviews_api():
  print(jwt_current_user.UniId) 
  student = get_student_by_UniId(jwt_current_user.UniId)

  # Check if the student exists
  if student:
    reviews = []
    for review in student.reviews:
      review_data = {
          'ID': review.ID,
          'studentID': review.studentID,
          'createdByStaffID': review.createdByStaffID,
          'isPositive': review.isPositive,
          'dateCreated': review.dateCreated.isoformat(),
          'points': review.points,
          'details': review.details
      }
      reviews.append(review_data)

    return jsonify({'reviews': reviews}), 200
  else:
    return jsonify({'message': 'Student not found'}), 404


@student_views.route('/view-all-incidents', methods=['GET'])
@login_required
def view_all_incidents():
  # Return the students' details in JSON format
  student = get_student_by_UniId(current_user.UniId)
  user = User.query.filter_by(ID=current_user.ID).first()
  if student:
    for incident in student.incidents:
      incident.studentSeen = True
      print(incident.studentSeen)
      db.session.add(incident)
      db.session.commit()
  return render_template('AllStudentIncidents.html'
                        , student=student
                         ,user=user)
  #return jsonify({'students': students_data}), 200


@student_views.route('/viewRR', methods=['GET'])
@login_required
def viewRR():
  student = get_student_by_UniId(current_user.UniId)
  recommendations = get_recommendations_student(current_user.UniId)
  user = User.query.filter_by(ID=current_user.ID).first() 
  if recommendations:
    for recommendation in recommendations:
      recommendation.studentSeen = True
      db.session.add(recommendation)
      db.session.commit()
  return render_template('AllRRs.html',
                         student=student,
                         recommendations=recommendations
                        , user=user)


@student_views.route('/api/view-all-incidents', methods=['GET'])
@jwt_required()
def view_all_incidents_api():
  # Return the students' details in JSON format
  student = get_student_by_UniId(jwt_current_user.UniId)

  # Check if the student exists
  if student:
    incidents = []
    for incident in student.incidents:
      incident_data = {
          'id': incident.id,
          'studentID': incident.studentID,
          'madeByStaffId': incident.madeByStaffId,
          'topic': incident.topic,
          'report': incident.report,
          'dateCreated': incident.dateCreated.isoformat(),
          'pointsDeducted': incident.pointsDeducted,
          'status': incident.studentSeen
      }
      incidents.append(incident_data)

    return jsonify({'incidents': incidents}), 200
  else:
    return jsonify({'message': 'Student not found'}), 404


@student_views.route('/view-all-achievements', methods=['GET'])
@login_required
def view_all_achievements():
  student = Student.query.filter_by(ID=current_user.ID).first()
  user = User.query.filter_by(ID=current_user.ID).first() 
  if student:
    for achievement in student.accomplishments:
      achievement.studentSeen = True
      print(achievement.studentSeen)
      db.session.add(achievement)
      db.session.commit()

  return render_template('AllStudentAchivements.html'
                        , student=student
                         ,user=user)
  #return jsonify({'students': students_data}), 200
