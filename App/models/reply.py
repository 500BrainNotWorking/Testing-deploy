class Reply(db.Model):
    __tablename__ = 'reply'

    ID = db.Column(db.Integer, primary_key=True)
    commentID = db.Column(db.Integer, db.ForeignKey('comment.ID'), nullable=False)  # Links to a comment
    createdByStaffID = db.Column(db.Integer, db.ForeignKey('staff.ID'), nullable=False)
    parentReplyID = db.Column(db.Integer, db.ForeignKey('reply.ID'), nullable=True) # This is used to determine if a reply is a reply to another reply, or a direct reply to a commnet (will be None in this case)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.String(400), nullable=False)  

    def __init__(self, commentID, staffID, details, parentReplyID=None):
        self.commentID = commentID
        self.createdByStaffID = staffID
        self.details = details
        self.dateCreated = datetime.utcnow()
        self.parentReplyID = parentReplyID