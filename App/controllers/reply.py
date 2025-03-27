from App.models import Reply
from App.models import Comment
from App.database import db
from datetime import datetime


def get_all_replies():
    return Reply.query.all()

def get_all_replies_comment(commentID):
    return Reply.query.filter_by(commentID=commentID).all()

def get_all_replies_staff(createdByStaffID):
    return Reply.query.filter_by(createdByStaffID=createdByStaffID).all()

def get_parent_reply(reply_id):
    reply = get_reply(reply_id)

    if reply and reply.parentReplyID is not None:
        parent_reply = get_reply(reply.parentReplyID)
        return parent_reply
    else:
        return None


#Use this function to get the very first reply in a thread of replies.
def get_root_parent_reply(reply_id):
    reply = get_reply(reply_id)

    if reply and reply.parentReplyID is not None:
        parent_reply = get_reply(reply.parentReplyID)
        return get_root_parent_reply(parent_reply.ID)
    else:
        return reply 

def get_reply(id):
    return Reply.query.filter_by(ID=id).first()



def create_reply(commentID, staffID, details, parentReplyID=None):
    new_reply = Reply(commentID=commentID, staffID=staffID, details=details, parentReplyID=parentReplyID) #If the parent ID field is left empty, 
                                                                                                        #then it is a direct reply. If the parent id field has a reply id, 
                                                                                                        #then its a response to another reply. The default is None, but this will be overridden.

    if new_reply:
        existing_comment = Comment.query.get(commentID)

        if existing_comment:
            existing_comment.replies.append(new_reply)
            db.session.add(new_reply)
            db.session.commit()
            return new_reply
        else:
            return None
    else:
        return None


def delete_reply(reply_id, staff_id):
    reply = get_reply(reply_id)
    if reply:
        if reply.createdByStaffID == staff_id:
            db.session.delete(reply)
            db.session.commit()
            return True
        else:
            return None
    else:
        return None

def edit_reply(details, reply_id, staff_id):
    
    existing_reply = get_reply(reply_id)
    if existing_reply:
        if existing_reply.createdByStaffID == staff_id:
            existing_reply.details = details
            existing_reply.dateCreated = datetime.now()
            db.session.add(existing_reply)
            db.session.commit()
            return True
        else:
            return None
    else:
        return None