from App.models import Review
from App.database import db


def create_review(staff, student, starRating, details):
  if starRating is None:
        return False
  
  isPositive = True if starRating >= 3 else False  # 3-5 = positive, 0-2 = negative
  newReview = Review(staff=staff,
                     student=student,
                     isPositive=isPositive,
                     starRating=starRating,
                     details=details,
                     studentSeen=False)
  db.session.add(newReview)
  try:
    db.session.commit()
    return True #Will have to change this to return the actual review created, and not just true and false
  except Exception as e:
    print("[review.create_review] Error occurred while creating new review: ",
          str(e))
    db.session.rollback()
    return False


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


def calculate_points_upvote(review):
  review.starRating *= 1.1  # multiplier can be changed accordingly

  try:
    db.session.commit()
    return True
  except Exception as e:
    print(
        "[review.calculate_points_upvote] Error occurred while updating review points:",
        str(e))
    db.session.rollback()
    return False


def calculate_points_downvote(review):
  review.starRating *= 0.9

  try:
    db.session.commit()
    return True
  except Exception as e:
    print(
        "[review.calculate_points_downvote] Error occurred while updating review points:",
        str(e))
    db.session.rollback()
    return False


# def get_total_review_points(studentID):
#   reviews = Review.query.filter_by(studentID=studentID).all()
#   if reviews:
#     sum = 0
#     for review in reviews:
#       sum += review.points
#     return sum
#   return 0

# Get the total starRating for positive reviews
def get_total_positive_review_starRating(studentID):
    reviews = Review.query.filter_by(studentID=studentID, isPositive=True).all()
    total_positive = sum(review.starRating for review in reviews)
    return total_positive

# Get the total starRating for negative reviews
def get_total_negative_review_starRating(studentID):
    reviews = Review.query.filter_by(studentID=studentID, isPositive=False).all()
    total_negative = sum(review.starRating for review in reviews)
    return total_negative

def get_reviews(studentID):
  reviews = Review.query.filter_by(studentID=studentID).all()                   #added this function for staff views (by A.M.)
  return reviews

def get_review(id):
  review = Review.query.filter_by(ID=id).first()
  if review:
    return review
  else:
    return None
  
# Get the count of unique reviewers (e.g., distinct staff or lecturers)
def get_unique_reviewers_count(studentID):
    # Query to get all reviews for the given student
    reviews = db.session.query(Review).filter(Review.studentID == studentID).all()

    # Use a set to store unique reviewers (staff or lecturer)
    unique_reviewers = set()

    # Loop through all reviews and add each unique staff/lecturer to the set
    for review in reviews:
        # Assuming each review has a 'staff' or 'lecturerID' field representing the reviewer
        unique_reviewers.add(review.createdByStaffID)  # 'staff' or 'lecturerID' should be the reviewer identifier

    # Return the count of unique reviewers
    return len(unique_reviewers)



def get_all_reviews():
  reviews = Review.query.all()
  return reviews