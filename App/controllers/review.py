from App.models import Review, Karma
from App.database import db
from .student import get_student_by_id
from datetime import datetime

def create_review(staff, student, starRating, details):
  if starRating is None:
        return False
  
  newReview = Review(staff=staff,
                     student=student,
                     starRating=starRating,
                     details=details)
  db.session.add(newReview)
  """Adjust the student's karma based on the star rating of the review."""
  if newReview.starRating == 5:
    points = 5
  elif newReview.starRating == 4:
    points = 3
  elif newReview.starRating == 3:
    points = 1
  elif newReview.starRating == 2:
    points = -1
  else:
    points = -3
  current_karma = student.get_karma()
  if current_karma:
    new_karma_points = current_karma.points + points
  else:
     new_karma_points = points
  newKarma = Karma(new_karma_points, student.ID)
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


def edit_review_work(details, review_id, staff_id, starRating):
    
    existing_review = get_review(review_id)
    if existing_review:

        if existing_review.createdByStaffID == staff_id:

            existing_review.details = details
            existing_review.starRating = starRating
            existing_review.dateCreated = datetime.now()
            db.session.add(existing_review)
            db.session.commit()
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
    new_karma_points = current_karma + review.starRating * ((review.likes - review.dislikes) / (4 * (review.likes + review.dislikes)))
    newKarma = Karma(new_karma_points, student.ID)
  db.session.add(newKarma)
  try:
    db.session.commit()
  except Exception as e:
    print(str(e))
    db.session.rollback()

def like(review_id):
  review = get_review(review_id)
  if review:
    review.likes += 1
    vote(review_id)

def dislike(review_id):
  review = get_review(review_id)
  if review:
    review.dislikes += 1
    vote(review_id)

# def get_total_review_points(studentID):
#   reviews = Review.query.filter_by(studentID=studentID).all()
#   if reviews:
#     sum = 0
#     for review in reviews:
#       sum += review.points
#     return sum
#   return 0

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
  reviews = Review.query.all()
  return reviews