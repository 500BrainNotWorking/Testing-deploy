from App.models import Karma, Student
from App.database import db
from .accomplishment import get_total_accomplishment_points
from .incidentReport import get_total_incident_points
from .transcript import calculate_academic_score
from sqlalchemy.exc import SQLAlchemyError

def get_karma(studentID):
    try:
        karma = Karma.query.filter_by(studentID=studentID).order_by(Karma.karmaID.desc()).first()
        return karma if karma else None
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_karma: {e}")
        return None

def get_karma_history(studentID):
    try:
        history = Karma.query.filter_by(studentID=studentID).order_by(Karma.karmaID.desc()).all()
        return history if history else None
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_karma_history: {e}")
        return None

def get_karma_student(student):
    try:
        karma = Karma.query.filter_by(studentID=student.ID).order_by(Karma.karmaID.desc()).first()
        return karma if karma else None
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_karma_student: {e}")
        return None

def create_karma(studentID, points, reviewID):
    try:
        newKarma = Karma(points=points, studentID=studentID, reviewID=reviewID)
        db.session.add(newKarma)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"[DB ERROR] create_karma: {e}")
        return False

def calculate_ranks():
    try:
        students = Student.query.all()
        student_karma = []

        for student in students:
            try:
                karma_value = student.get_karma().points if student.get_karma() else 0
                student_karma.append((karma_value, student.ID))
            except Exception as inner_e:
                print(f"[ERROR] student.get_karma failed for student {student.ID}: {inner_e}")
                student_karma.append((0, student.ID))

        student_karma.sort(reverse=True, key=lambda x: x[0])

        for rank, (karma, student_id) in enumerate(student_karma, start=1):
            try:
                student = Student.query.get(student_id)
                student.update(rank)
            except Exception as update_e:
                print(f"[ERROR] Failed to update rank for student {student_id}: {update_e}")

    except SQLAlchemyError as e:
        print(f"[DB ERROR] calculate_ranks: {e}")
