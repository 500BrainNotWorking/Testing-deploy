from App.models import Comment
from App.models import Review
from App.models import Staff
from App.database import db
from datetime import datetime
from .reply import delete_reply
from sqlalchemy.exc import SQLAlchemyError

def get_all_comments():
    try:
        return Comment.query.all()
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_all_comments: {e}")
        return []

def get_all_comments_review(reviewID):
    try:
        return Comment.query.filter_by(reviewID=reviewID).all()
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_all_comments_review: {e}")
        return []

def get_comment_staff(createdByStaffID):
    try:
        return Comment.query.filter_by(createdByStaffID=createdByStaffID).all()
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_comment_staff: {e}")
        return []

def get_comment(id):
    try:
        return Comment.query.filter_by(ID=id).first()
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_comment: {e}")
        return None

def create_comment(reviewID, staffID, details):
    try:
        new_comment = Comment(reviewID=reviewID, staffID=staffID, details=details) 
        new_comment.replies = []

        if new_comment:
            existing_review = Review.query.get(reviewID)

            if existing_review:
                existing_review.comments.append(new_comment)
                db.session.add(new_comment)
                db.session.commit()
                return new_comment
            else:
                return None
        else:
            return None
    except SQLAlchemyError as e:
        print(f"[DB ERROR] create_comment: {e}")
        db.session.rollback()
        return None

def delete_comment(comment_id, staff_id):
    try:
        comment = get_comment(comment_id)
        if comment:
            if comment.createdByStaffID == staff_id:
                for reply in comment.replies:
                    delete_reply(reply.ID, staff_id)
                db.session.delete(comment)
                db.session.commit()
                return True
            else:
                return None
        else:
            return None
    except SQLAlchemyError as e:
        print(f"[DB ERROR] delete_comment: {e}")
        db.session.rollback()
        return None

def edit_comment(details, comment_id, staff_id):
    try:
        existing_comment = get_comment(comment_id)
        if existing_comment:
            if existing_comment.createdByStaffID == staff_id:
                existing_comment.details = details
                existing_comment.dateCreated = datetime.now()
                db.session.add(existing_comment)
                db.session.commit()
                return True
            else:
                return None
        else:
            return None
    except SQLAlchemyError as e:
        print(f"[DB ERROR] edit_comment: {e}")
        db.session.rollback()
        return None
