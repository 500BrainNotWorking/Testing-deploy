from App.models import Review, Karma
from App.database import db
from .student import get_student_by_id
from datetime import datetime

from .comment import delete_comment

import ast

def create_review(staff, student, starRating, details):
  if starRating is None:
        return False
  
  newReview = Review(staff=staff,
                     student=student,
                     starRating=starRating,
                     details=details)

  newReview.comments=[]
  db.session.add(newReview)
  """Adjust the student's karma based on the star rating of the review."""
  current_karma = student.get_karma()
  if current_karma:
    new_karma_points = current_karma.points + newReview.value
  else:
     new_karma_points = newReview.value
  newKarma = Karma(new_karma_points, student.ID, newReview.ID)
  db.session.add(newKarma)
  try:
    db.session.commit()
    return newReview
  except Exception as e:
      print(str(e))
      db.session.rollback()



def delete_review(reviewID):
  review = Review.query.filter_by(ID=reviewID).first()
  if review:
    db.session.delete(review)
    try:
      db.session.commit()
      return True
    except Exception as e:
      print("[review.delete_review] Error occurred while deleting review: ",
            str(e))
      db.session.rollback()
      return False
  else:
    return False


def delete_review_work(review_id, staff_id):
    review = get_review(review_id)
    if review:
        if review.createdByStaffID == staff_id:
            for comment in review.comments:
              delete_comment(comment.ID, staff_id)
            db.session.delete(review)
            db.session.commit()
            return True
        else:
            return None
    else:
        return None


def edit_review_work(details, review_id, staff_id, starRating):
    
    existing_review = get_review(review_id)
    if existing_review:

        if existing_review.createdByStaffID == staff_id:

            existing_review.details = details
            existing_review.starRating = starRating
            existing_review.dateCreated = datetime.now()
            db.session.add(existing_review)
            db.session.commit()
            return True
        else:
            return None
    else:
        return None

  
def edit_review(reviewID, starRating, details):
  review = get_review(reviewID)
  if review:
    review.details = details
    review.starRating = starRating
    try:
      db.session.commit()
    except Exception as e:
      print("Could not edit review", str(e))
      db.session.rollback()

def get_reviews_for_student(student_id):
  student = get_student_by_id(student_id)
  if student:
    return student.reviews
  return None

def get_recent_reviews(top):
  reviews = Review.query.order_by(Review.dateCreated.desc()).limit(top).all()
  return reviews

def vote(review_id):
  review = get_review(review_id)
  if review:
    student = get_student_by_id(review.studentID)
    current_karma = student.get_karma()
    new_karma_points = current_karma.points + review.starRating * ((review.likes - review.dislikes) / (4 * (review.likes + review.dislikes)))
    newKarma = Karma(new_karma_points, student.ID, review.ID)
  db.session.add(newKarma)
  try:
    db.session.commit()
  except Exception as e:
    print(str(e))
    db.session.rollback()

def like(review_id, staff_id):
  review = get_review(review_id)

  liked_by_staff = ast.literal_eval(review.liked_by_staff or '[]')
  disliked_by_staff = ast.literal_eval(review.disliked_by_staff or '[]')

  staff_id = str(staff_id)

  #print(review.liked_by_staff)

  if staff_id in review.liked_by_staff:
    #print('already liked')
    return False

  if staff_id in review.disliked_by_staff:
    #print ('change to likes')
    disliked_by_staff.remove(staff_id)
    review.dislikes = review.dislikes - 1

    review.likes = review.likes +1
    vote(review_id)
    liked_by_staff.append(staff_id)
  else:
    #print('already in likes')
    review.likes = review.likes +1
    vote(review_id)
    liked_by_staff.append(staff_id)

  
  review.liked_by_staff = str(liked_by_staff)
  review.disliked_by_staff = str(disliked_by_staff)

  staff_id = int(staff_id)


  db.session.commit()
  return True



  # if review:
  #   review.likes += 1
  #   vote(review_id)

def dislike(review_id, staff_id):

  review = get_review(review_id)

  liked_by_staff = ast.literal_eval(review.liked_by_staff or '[]')
  disliked_by_staff = ast.literal_eval(review.disliked_by_staff or '[]')

  staff_id = str(staff_id)

  #print(review.disliked_by_staff)

  if staff_id in review.disliked_by_staff:
    #print('already disliked')
    return False

  if staff_id in review.liked_by_staff:
    #print('change to likes likes')
    liked_by_staff.remove(staff_id)
    review.likes = review.likes - 1

    review.dislikes = review.dislikes +1
    vote(review_id)
    disliked_by_staff.append(staff_id)
  else:
    #print('already in dislikes')
    review.dislikes = review.dislikes +1
    vote(review_id)
    disliked_by_staff.append(staff_id)


  review.liked_by_staff = str(liked_by_staff)
  review.disliked_by_staff = str(disliked_by_staff)

  staff = int(staff_id)



  db.session.commit()
  return True


  db.session.commit()
  return True

def get_reviews(studentID):
  reviews = Review.query.filter_by(studentID=studentID).all()                   #added this function for staff views (by A.M.)
  return reviews

def get_review(id):
  review = Review.query.filter_by(ID=id).first()
  if review:
    return review
  else:
    return None

def get_all_reviews():
  reviews = Review.query.order_by(Review.dateCreated.desc()).all() #Review.query.all()
  return reviews