from App.models import Review, Karma
from App.database import db
from .student import get_student_by_id
from datetime import datetime
from .comment import delete_comment
import ast
from sqlalchemy.exc import SQLAlchemyError

review_factor = 0.25

def create_review(staff, student, starRating, details):
  if starRating is None:
        return False
  
  newReview = Review(staff=staff,
                     student=student,
                     starRating=starRating,
                     details=details)

  newReview.comments=[]
  db.session.add(newReview)
  
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
  except SQLAlchemyError as e:
      print(f"[DB ERROR] create_review: {e}")
      db.session.rollback()
      return None


def delete_review(reviewID):
  review = Review.query.filter_by(ID=reviewID).first()
  if review:
    db.session.delete(review)
    try:
      db.session.commit()
      return True
    except SQLAlchemyError as e:
      print(f"[DB ERROR] delete_review: {e}")
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
            try:
                db.session.delete(review)
                db.session.commit()
                return True
            except SQLAlchemyError as e:
                print(f"[DB ERROR] delete_review_work: {e}")
                db.session.rollback()
                return False
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
            try:
                db.session.commit()
                return True
            except SQLAlchemyError as e:
                print(f"[DB ERROR] edit_review_work: {e}")
                db.session.rollback()
                return False
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
    except SQLAlchemyError as e:
      print(f"[DB ERROR] edit_review: {e}")
      db.session.rollback()


def get_reviews_for_student(student_id):
  try:
    student = get_student_by_id(student_id)
    if student:
      return student.reviews
  except Exception as e:
    print(f"[ERROR] get_reviews_for_student: {e}")
  return None


def get_recent_reviews(top):
  try:
    reviews = Review.query.order_by(Review.dateCreated.desc()).limit(top).all()
    return reviews
  except SQLAlchemyError as e:
    print(f"[DB ERROR] get_recent_reviews: {e}")
    return []


def like(review_id, staff_id):
  try:
    review = get_review(review_id)

    liked_by_staff = ast.literal_eval(review.liked_by_staff or '[]')
    disliked_by_staff = ast.literal_eval(review.disliked_by_staff or '[]')
    student = get_student_by_id(review.studentID)
    staff_id = str(staff_id)

    if staff_id in review.liked_by_staff:
      return False

    current_karma = student.get_karma()
    new_karma_points = current_karma.points
    if staff_id in review.disliked_by_staff:
      disliked_by_staff.remove(staff_id)
      new_karma_points += review_factor * review.value / review.dislikes
      review.dislikes -= 1
      review.likes += 1
      liked_by_staff.append(staff_id)
    else:
      review.likes += 1
      liked_by_staff.append(staff_id)

    new_karma_points += review_factor * review.value / review.likes
    newKarma = Karma(new_karma_points, student.ID, review.ID)
    db.session.add(newKarma)

    review.liked_by_staff = str(liked_by_staff)
    review.disliked_by_staff = str(disliked_by_staff)

    db.session.commit()
    return True
  except SQLAlchemyError as e:
    print(f"[DB ERROR] like: {e}")
    db.session.rollback()
    return False


def dislike(review_id, staff_id):
  try:
    review = get_review(review_id)

    liked_by_staff = ast.literal_eval(review.liked_by_staff or '[]')
    disliked_by_staff = ast.literal_eval(review.disliked_by_staff or '[]')
    student = get_student_by_id(review.studentID)
    staff_id = str(staff_id)

    if staff_id in review.disliked_by_staff:
      return False

    current_karma = student.get_karma()
    new_karma_points = current_karma.points
    if staff_id in review.liked_by_staff:
      liked_by_staff.remove(staff_id)
      new_karma_points -= review_factor * review.value / review.likes
      review.likes -= 1
      review.dislikes += 1
      disliked_by_staff.append(staff_id)
    else:
      review.dislikes += 1
      disliked_by_staff.append(staff_id)

    new_karma_points -= review_factor * review.value / review.dislikes
    newKarma = Karma(new_karma_points, student.ID, review.ID)
    db.session.add(newKarma)

    review.liked_by_staff = str(liked_by_staff)
    review.disliked_by_staff = str(disliked_by_staff)

    db.session.commit()
    return True
  except SQLAlchemyError as e:
    print(f"[DB ERROR] dislike: {e}")
    db.session.rollback()
    return False


def get_reviews(studentID):
  try:
    reviews = Review.query.filter_by(studentID=studentID).all()
    return reviews
  except SQLAlchemyError as e:
    print(f"[DB ERROR] get_reviews: {e}")
    return []


def get_review(id):
  try:
    review = Review.query.filter_by(ID=id).first()
    return review if review else None
  except SQLAlchemyError as e:
    print(f"[DB ERROR] get_review: {e}")
    return None


def get_all_reviews():
  try:
    reviews = Review.query.order_by(Review.dateCreated.desc()).all()
    return reviews
  except SQLAlchemyError as e:
    print(f"[DB ERROR] get_all_reviews: {e}")
    return []
