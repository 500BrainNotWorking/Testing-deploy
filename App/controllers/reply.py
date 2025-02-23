from App.models import Reply
from App.models import Comment
from App.database import db


def get_all_repliess():
    return Reply.query.all()

def get_reply(id):
    return Reply.query.filter_by(ID=id).first()

def create_reply(reviewID, staffID, details):
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


def create_reply(commentID, staffID, details, parentReplyID=None):
    new_reply = Reply(commentID=commentID, staffID=staffID, details=details, parentReplyID=parentReplyID) #If the parent ID field is left empty, 
                                                                                                        #then it is a direct reply. If the parent id field has a reply id, 
                                                                                                        #then its a response to another reply. The default is None, but this will be overridden.

    if new_reply:
        existing_comment = Comment.query.get(commentID)

        if existing_comment:
            existing_comment.replies.append(new_comment)
            db.session.add(new_reply)
            db.session.commit()
            return new_reply
        else:
            return None
    else:
        return None


def delete_reply(reply_id):
    reply = get_reply(reply_id)
    if reply:
        db.session.delete(reply)
        db.session.commit()
    else:
        return None

def edit_reply(details, reply_id):
    
    existing_reply = get_reply(reply_id)
    if existing_reply:
        
        existing_reply.details = details
        db.session.add(existing_reply)
        db.session.commit()
    else:
        return None