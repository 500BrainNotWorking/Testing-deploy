from App.models import Staff, Review, Student
from App.database import db 
import os
from werkzeug.utils import secure_filename

from .review import (
    create_review,
    get_review
)
from .student import(
    get_student_by_id,
    get_student_by_username,
    get_students_by_degree,
    get_students_by_faculty
)

def create_staff(username,firstname, lastname, email, password, faculty):
    newStaff = Staff(username,firstname, lastname, email, password, faculty)
    db.session.add(newStaff)
    
    try:
        db.session.commit()
        return True
        # can return if we need
        # return newStaff
    except Exception as e:
        print("[staff.create_staff] Error occurred while creating new staff: ", str(e))
        db.session.rollback()
        return False
    

def get_staff_by_id(id):
    staff = Staff.query.filter_by(ID=id).first()
    if staff:
        return staff
    else:
        return None

def get_staff_by_name(firstname, lastname):
  staff = Staff.query.filter_by(firstname=firstname, lastname=lastname).first()
  if staff:
      return staff
  else:
      return None

def get_staff_by_username(username):
    staff = Staff.query.filter_by(username=username).first()
    if staff:
        return staff
    else:
        return None

def staff_edit_review(id, details):
    review = get_review(id)
    if review is None:
        return False
    else:
        review.details = details
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[staff.staff_edit_review] Error occurred while editing review:", str(e))
            db.session.rollback()
            return False


def staff_create_review(staff, student, starRating, details):
    if create_review(staff, student, starRating,details):
        return True
    else:
        return False


import os
from werkzeug.utils import secure_filename
from App.database import db
from App.models.staff import Staff

def update_staff_profile(staff_id, firstname, lastname, faculty, email, profile_pic=None):
    staff = Staff.query.get(staff_id)

    if not staff:
        raise ValueError("Staff not found")

    staff.firstname = firstname
    staff.lastname = lastname
    staff.faculty = faculty
    staff.email = email

    if profile_pic and profile_pic.filename:
        filename = secure_filename(profile_pic.filename)
        # This is relative to the root directory of your app
        upload_dir = os.path.join('App', 'static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        upload_path = os.path.join(upload_dir, filename)
        profile_pic.save(upload_path)

        # This is the path used by HTML <img src="">
        staff.profile_pic = f'/static/uploads/{filename}'

    db.session.commit()


