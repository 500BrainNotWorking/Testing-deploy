from App.models import Comment
from App.models import Review
from App.database import db


def get_all_comments():
    return Comment.query.all()

def get_comment(id):
    return Comment.query.filter_by(ID=id).first()

def create_comment(reviewID, staffID, details):
    new_comment= Comment(reviewID=reviewID, staffID=staffID, details=details) 

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


def delete_comment(comment_id):
    comment = get_comment(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
    else:
        return None