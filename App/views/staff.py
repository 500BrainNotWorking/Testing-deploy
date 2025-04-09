from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, make_response
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.database import db
from flask_login import login_required, current_user
from sqlalchemy import or_
from datetime import datetime
import textwrap

from App.models import Student, Staff, User, IncidentReport, Review, Comment, Reply

from App.controllers import (
    jwt_authenticate, create_incident_report, get_student_by_UniId,
    get_accomplishment, get_student_by_id, get_recommendations_staff,
    get_recommendation, get_staff_by_id, get_students_by_faculty,
    get_staff_by_id, get_requested_accomplishments, get_transcript,
    get_total_As, get_student_for_ir, create_review, get_karma,
    get_requested_accomplishments_count,
    get_recommendations_staff_count, calculate_ranks, get_all_verified, 
    get_reviews, get_review, edit_review, edit_review_work, delete_review_work,
    create_comment, get_comment, get_comment_staff,
    get_reply, create_reply, get_all_reviews, create_staff, get_student_review_index, get_karma_history,
    like, dislike, update_staff_profile, get_all_students_json)            #added get_reviews


staff_views = Blueprint('staff_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''

@staff_views.route('/edit-profile/<int:staff_id>', methods=['GET'])
def edit_staff_profile_route(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        flash("Staff not found.", "error")
        return redirect(request.referrer)

    return render_template('EditProfile.html', staff=staff)


@staff_views.route('/update-staff-profile', methods=['POST'])
def update_staff_profile_route():
    staff_id = request.form.get('staff_id')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    faculty = request.form.get('faculty')
    email = request.form.get('email')
    profile_pic = request.files.get('profile_pic')

    try:
        # Assume this function updates everything and handles the image too
        update_staff_profile(
            staff_id=staff_id,
            firstname=firstname,
            lastname=lastname,
            faculty=faculty,
            email=email,
            profile_pic=profile_pic
        )

        flash("Profile updated successfully!", "success")
        return redirect(url_for('staff_views.staff_profile', staff_id=staff_id))
    except Exception as e:
        print(f"Error updating profile: {e}")
        flash("Something went wrong while updating the profile.", "error")
        return redirect(url_for('staff_views.getAllReviews'))



@staff_views.route('/like/<int:review_id>', methods=['POST'])
def like_review(review_id):
    # review = Review.query.get(review_id)
    # review.likes += 1
    # db.session.commit()

    like(review_id, current_user.get_id())
    return redirect(request.referrer)

@staff_views.route('/dislike/<int:review_id>', methods=['POST'])
def dislike_review(review_id):
    # review = Review.query.get(review_id)
    # review.dislikes += 1
    # db.session.commit()
    dislike(review_id, current_user.get_id())
    return redirect(request.referrer)


@staff_views.route('/viewKarmaDetail/<int:karma_id>', methods=['GET'])
@login_required
def view_karma_detail(karma_id):
    karma = get_karma_by_id(karma_id)  # Fetch karma entry from DB

    if karma is None:
        flash("Karma record not found.", "error")
        return redirect(url_for('staff_views.getAllReviews'))  # Redirect if invalid

    return redirect(url_for('staff_views.getAllReviews'))

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

@staff_views.route('/students/<int:student_id>/reviews/<int:review_index>', methods=['GET'])
def review_detail(student_id, review_index):
    student = get_student_by_UniId(student_id)
    if student:
        if review_index in range(len(student.reviews)):
            review_id = student.get_review_id(review_index)
            review = get_review(review_id)
            if review:
                staff = get_staff_by_id(review.createdByStaffID)
                review.staff_name = f"{staff.firstname} {staff.lastname}" if staff else "Unknown Staff"
                review.student_name = student.fullname
                review.student_id = student.UniId
                review.staffpic = staff.profile_pic

                comment_staffs = []
                replier_staffs = []

                for comment in review.comments:
                    comment_staffs.append(get_comment_staff(comment.createdByStaffID))
                    
                    replier_list = []
                    for reply in comment.replies:
                        replier_list.append(get_comment_staff(reply.createdByStaffID))
                    replier_staffs.append(replier_list)

                comment_info = zip(review.comments, comment_staffs)
                return render_template('ReviewDetail.html', review=review, comment_info=comment_info, replier_staffs=replier_staffs, get_staff=get_staff_by_id)
            else:
                flash("Review does not exist", "error")
    else:
        flash("Student does not exist", "error")
    return redirect('/getMainPage')


@staff_views.route('/reviews/<int:review_id>', methods=['POST'])
@login_required
def post_comment(review_id):
  content = request.form
  review = get_review(review_id)
  if current_user.user_type == 'staff':
    details = content['details']
    details = "\n".join(textwrap.wrap(details, width=80))  # Wrap text at 80 characters

    create_comment(review_id, current_user.ID, details)
    return redirect(f"/reviews/{review.ID}")
  else:
     flash("Must be logged in as staff", "error")
     return redirect('/login')

@staff_views.route('/reviews/<int:review_id>', methods=['GET'])
@login_required
def expand_review(review_id):
  review = get_review(review_id)
  if review:
    student = get_student_by_id(review.studentID)
    review_index = get_student_review_index(student.ID, review.ID)
    return redirect(f"/students/{student.UniId}/reviews/{review_index}")
  else:
     flash("Review does not exist", "error")
     return redirect('/getMainPage')

@staff_views.route('/comments/<int:comment_id>', methods=['POST'])
@login_required
def post_reply(comment_id):
  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id)
  if staff:
    data = request.form
    details = data['reply-details']
    details = "\n".join(textwrap.wrap(details, width=80))  # Wrap text at 80 characters

    comment = get_comment(comment_id)

    if comment:
        create_reply(commentID=comment_id, staffID=staff_id, details=details, parentReplyID=None)
        return redirect(f"/reviews/{comment.reviewID}")
    else:
        error = f"Comment is not found!"
  else:
    error = f"You are not logged in as staff and cannot post a Reply!"
  flash(error, "error")
  return redirect('/getMainPage')
   
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

@staff_views.route('/viewReplies/<int:comment_id>', methods=['GET'])
@login_required
def view_all_replies(comment_id):
  comment = get_comment(comment_id)
  #user = User.query.filter_by(ID=current_user.ID).first()

  replies = get_all_replies()

  return render_template('', comments=comments, review=review)# Put the appropriate template here, and current_user if needed.


@staff_views.route('/editReply/<int:reply_id>', methods=['POST'])
@login_required
def edit_reply(reply_id):
  reply = get_reply(reply_id)
  #user = User.query.filter_by(ID=current_user.ID).first()

  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id) 

  data = request.form #Depening on how the create comment form is made/designed this si subject to change, along with attribute names.

  details = data['selected-details']

  edit_reply(details=details, reply_id=reply_id, staff_id=staff_id)

  return render_template('',current_user=current_user)# Put the appropriate template here, and current_user if needed.

@staff_views.route('/deleteReply/<int:reply_id>', methods=['GET'])
@login_required
def delete_reply(reply_id):
  reply = get_reply(reply_id)
  #user = User.query.filter_by(ID=current_user.ID).first()

  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id) 

  delete_reply(reply_id=reply_id, staff_id=staff_id)

  return render_template('',current_user=current_user)# Put the appropriate template here, and current_user if needed.


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

@staff_views.route('/editComment/<int:comment_id>', methods=['POST'])
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
  
#from flask import flash, redirect, url_for, render_template

@staff_views.route('/createReview', methods=['POST'])
@login_required
def createReview():
    staff_id = current_user.get_id()
    staff = get_staff_by_id(staff_id)

    data = request.form
    studentID = data['studentID']
    studentName = data['name']
    points = int(data['points'])
    num = data['num']
    personalReview = data['manual-review']
    details = data['selected-details']

    # Ensure studentName is valid before splitting
    if ' ' in studentName:
        firstname, lastname = studentName.split(' ', 1)
    else:
        firstname, lastname = studentName, ""

    student = get_student_by_UniId(studentID)

    if personalReview:
        wrapped_review = "\n".join(textwrap.wrap(personalReview, width=80))  # Wrap text at 80 characters
        details += f"{wrapped_review}"
        points += int(data.get('starRating', 0))  # Ensure default value if missing

    positive = points > 0  # Determine review positivity

    if student:
        review = create_review(staff, student, points, details)
        flash(f"Successfully created a review for {studentName}!", "success")
    else:
        flash(f"Error creating review for {studentName}. Please check student details.", "error")

    return redirect(request.referrer)  # Redirect to the create review page

@staff_views.route('/deleteReview/<int:review_id>', methods=['GET'])
@login_required
def delete_review(review_id):
  review = get_review(review_id)
  #user = User.query.filter_by(ID=current_user.ID).first()

  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id) 

  # if review:
  #   delete_review_work(review_id=review_id, staff_id=staff_id) 
  #   flash(f"Successfully deleted a review!", "success")

  if review:
    delete_review_work(review_id=review_id, staff_id=staff_id) 
    flash(f"Successfully deleted review!", "success")
  else:
    flash(f"Error deleting review.", "error")

  return redirect(url_for('staff_views.getAllReviews'))# Put the appropriate template here, and current_user if needed.




@staff_views.route('/editReview/<review_id>', methods=['POST'])
@login_required
def edit_review(review_id):
  review = get_review(review_id)
  #user = User.query.filter_by(ID=current_user.ID).first()

  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id) 

  data = request.form
  #studentID = data['studentID']
  #studentName = data['name']
  points = int(data['points'])
  num = data['num']
  personalReview = data['manual-review']
  details = data['selected-details']

  starRating = data['selectedRating']

  if personalReview:
        details += f"{personalReview}"
        points += int(data.get('starRating', 0))  # Ensure default value if missing

  #data = request.form #Depening on how the create comment form is made/designed this si subject to change, along with attribute names.

  #details = data['selected-details']

  if review:
    edit_review_work(details=details, review_id=review_id, staff_id=staff_id, starRating=starRating)
    print("work")
    flash(f"Successfully edited review!", "success")
  else:
    flash(f"Error editing review for {review_id}. Please check student details.", "error")
  
  #if review:

    #edit_review(details=details, review_id=review_id, staff_id=staff_id) Changes Need to be made to the review controller so it checks
                                                                      #That the correct staff is attempting to edit the review.
                                                                      # There needs to be an extra parameter passed, which is the staff_id.

  return redirect(url_for('staff_views.getAllReviews'))# Put the appropriate template here, and current_user if needed.


@staff_views.route('/createReviewPage', methods=['GET'])
@login_required
def create_review_page():
    return render_template('CreateReview.html')


@staff_views.route('/editReviewPage/<id>', methods=['GET'])
@login_required
def edit_review_page(id):

  sel_review = get_review(id)

  sel_student = get_student_by_id(sel_review.studentID)

  return render_template('EditReview.html', sel_review= sel_review, sel_student=sel_student)



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

@staff_views.route('/students')
@staff_views.route('/students/<int:uni_id>')
@login_required
def view_students(uni_id=-1):
  students = get_all_students_json()
  if uni_id == -1:
    selected_student = get_student_by_id(students[0]['id'])
  else:
    selected_student = get_student_by_UniId(uni_id)
    
  reviews = selected_student.reviews
  for review in reviews:
        staff = get_staff_by_id(review.createdByStaffID)  # Get Staff object
        review.staff_name = staff.firstname + " " + staff.lastname if staff else "Unknown Staff"  # Attach fullname
        review.staffpic = staff.profile_pic
  
  students.sort(key = lambda e: e['firstname'])
  return render_template('AllStudents.html', students=students, selected_student=selected_student, reviews=reviews)
  

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
        calculate_ranks()
        # student.update(karma.rank)
        # karma.notify()

    transcripts = get_transcript(student.UniId)
    numAs = get_total_As(student.UniId)
    reviews = get_reviews(student.ID)

    karma_history = get_karma_history(student.ID)

    # Attach staff name dynamically
    for review in reviews:
        staff = get_staff_by_id(review.createdByStaffID)  # Get Staff object
        review.staff_name = staff.firstname + " " + staff.lastname if staff else "Unknown Staff"  # Attach fullname
        review.staffpic = staff.profile_pic

    review_links = []
    for review in reviews:
        index = get_student_review_index(student.ID, review.ID)
        review_links.append(index)


    return render_template('Student-Profile-forStaff.html',
                           student=student,
                           user=user,
                           transcripts=transcripts,
                           numAs=numAs,
                           karma=karma,
                           reviews=reviews,
                           history = karma_history,
                           review_links = review_links)


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







@staff_views.route('/getMainPage', methods=['GET'])
@login_required
def getAllReviews():
    
    reviews = get_all_reviews()

    # Attach staff name dynamically
    for review in reviews:
        staff = get_staff_by_id(review.createdByStaffID)  # Get Staff object
        review.staff_name = staff.firstname + " " + staff.lastname if staff else "Unknown Staff"  # Attach fullname
        review.staffpic = staff.profile_pic

    for review in reviews:
        student = get_student_by_id(review.studentID)
        review.student_name = student.fullname if student else "Unknown Student"  # Attach fullname
        review.student_id = student.UniId if student else "Unknown ID"

    return render_template('MainPage.html',
                           reviews=reviews, current_user=current_user)

@staff_views.route('/staff-profile', methods=['GET'])
@login_required
def staff_profile():
    staff_id = current_user.get_id()  # Get logged-in staff ID
    staff = get_staff_by_id(staff_id)  # Fetch staff details

    if not staff:
        flash("Staff not found.", "error")
        return redirect(url_for('staff_views.get_StaffHome_page'))

    # Fetch reviews written by this staff member
    reviews = Review.query.filter_by(createdByStaffID=staff_id).all()

    # Create a list of formatted student names corresponding to each review
    student_names = []
    for review in reviews:
        student = get_student_by_id(review.studentID)
        if student:
            student_names.append(f"{student.fullname} ({student.UniId})")
        else:
            student_names.append("Unknown Student")

    return render_template('StaffProfile.html', staff=staff, reviews=reviews, student_names=student_names)



@staff_views.route('/staff-profile/<int:ID>', methods=['GET', 'POST'])
@login_required
def staff_profile_by_id(ID):
    staff = get_staff_by_id(ID)  # Fetch staff details

    if not staff:
        flash("Staff not found.", "error")
        return redirect(url_for('staff_views.get_StaffHome_page'))

    # Fetch reviews written by this staff member
    reviews = Review.query.filter_by(createdByStaffID=ID).all()

    # Create a list of formatted student names corresponding to each review
    student_names = []
    for review in reviews:
        student = get_student_by_id(review.studentID)
        if student:
            student_names.append(f"{student.fullname} ({student.UniId})")
        else:
            student_names.append("Unknown Student")

    return render_template('StaffProfile.html', staff=staff, reviews=reviews, student_names=student_names)




@staff_views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        faculty = request.form['faculty']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('SignUp.html', message="Passwords do not match!")

        # Save user to the database
        create_staff(
            firstname=firstname, lastname=lastname,
            faculty=faculty, username=username,
            email=email, password=password
        )

        return render_template('login.html') # Redirect to login after signup

    return render_template('SignUp.html')



@staff_views.route('/jsreview/<int:review_id>', methods=['GET'])
@login_required
def js_review_detail(review_id):
    # Retrieve the review using its ID
    review = get_review(review_id)
    if not review:
        flash("Review not found.", "error")
        return redirect(url_for('staff_views.getAllReviews'))
    
    # Retrieve the associated student using the correct attribute name:
    student = get_student_by_id(review.studentID)  # Use 'studentID' here
    if not student:
        flash("Associated student not found.", "error")
        return redirect(url_for('staff_views.getAllReviews'))
    
    # Retrieve the staff member who created the review and attach their full name.
    staff_member = get_staff_by_id(review.createdByStaffID)
    review.staff_name = f"{staff_member.firstname} {staff_member.lastname}" if staff_member else "Unknown Staff"
    
    # Attach the student's full name for display in the template.
    review.student_name = student.fullname if student else "Unknown Student"
    # IMPORTANT: Set review.student_id (used in your template link) to the student's UniId.
    review.student_id = student.UniId
    
    # Format the review date if needed.
    if review.dateCreated:
        review.dateCreated = review.dateCreated.strftime('%Y-%m-%d %H:%M:%S')
    
    # Render the ReviewDetail page using your provided template.
    return render_template('ReviewDetail.html', review=review)

@staff_views.route('/search-students', methods=['GET'])
def search_students():
    query = request.args.get('q', '')
    students = Student.query.filter(
        (Student.firstname.ilike(f'%{query}%')) |
        (Student.lastname.ilike(f'%{query}%')) |
        ((Student.firstname + ' ' + Student.lastname).ilike(f'%{query}%'))
    ).all()

    results = [{
        "id": s.UniId,
        "name": f"{s.firstname} {s.lastname}"
    } for s in students]

    return jsonify(results)
