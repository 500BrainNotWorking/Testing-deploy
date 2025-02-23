from App.models import Comment
from App.models import Review
from App.database import db

def create_comment(reviewID, staffID, details):
    new_comment= Comment(reviewID=reviewID, staffID=staffID, details=details) 

    if new_comment:
        existing_review = Review.query.get(reviewId)

        if existing_review:
            existing_review.comments.append(new_comment)
            db.session.add(new_comment)
            db.session.commit()
            return new_comment
        else:
            return None
    else:
        return None
 