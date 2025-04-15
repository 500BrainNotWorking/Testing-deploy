from App.models import Reply
from App.models import Comment
from App.database import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

def get_all_replies():
    try:
        return Reply.query.all()
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_all_replies: {e}")
        return []

def get_all_replies_comment(commentID):
    try:
        return Reply.query.filter_by(commentID=commentID).all()
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_all_replies_comment: {e}")
        return []

def get_all_replies_staff(createdByStaffID):
    try:
        return Reply.query.filter_by(createdByStaffID=createdByStaffID).all()
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_all_replies_staff: {e}")
        return []

def get_reply(id):
    try:
        return Reply.query.filter_by(ID=id).first()
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_reply: {e}")
        return None

def get_parent_reply(reply_id):
    try:
        reply = get_reply(reply_id)
        if reply and reply.parentReplyID is not None:
            parent_reply = get_reply(reply.parentReplyID)
            return parent_reply
        return None
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_parent_reply: {e}")
        return None

def get_root_parent_reply(reply_id):
    try:
        reply = get_reply(reply_id)
        if reply and reply.parentReplyID is not None:
            parent_reply = get_reply(reply.parentReplyID)
            return get_root_parent_reply(parent_reply.ID)
        return reply
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_root_parent_reply: {e}")
        return None

def create_reply(commentID, staffID, details, parentReplyID=None):
    try:
        new_reply = Reply(commentID=commentID, staffID=staffID, details=details, parentReplyID=parentReplyID)

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
    except SQLAlchemyError as e:
        print(f"[DB ERROR] create_reply: {e}")
        db.session.rollback()
        return None

def delete_reply(reply_id, staff_id):
    try:
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
    except SQLAlchemyError as e:
        print(f"[DB ERROR] delete_reply: {e}")
        db.session.rollback()
        return None

def edit_reply(details, reply_id, staff_id):
    try:
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
    except SQLAlchemyError as e:
        print(f"[DB ERROR] edit_reply: {e}")
        db.session.rollback()
        return None
