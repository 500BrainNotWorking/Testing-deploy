from App.models import User, Student
from App.database import db

def create_user(username, firstname, lastname, password, email, faculty):
    newuser = User(username=username, firstname=firstname, lastname=lastname, password=password, email=email, faculty=faculty)
    db.session.add(newuser)
    try:
        db.session.commit()
        return newuser
    except Exception as e:
        print("[user.create_user] Error occurred while creating new user: ", str(e))
        db.session.rollback()
        return None
    

def get_user_by_username(username):
    try:
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return None
    except Exception as e:
        print("[user.get_user_by_username] Error occurred: ", str(e))
        return None


def get_user(id):
    try:
        user = User.query.get(id)
        if user:
            return user
        else:
            return None
    except Exception as e:
        print("[user.get_user] Error occurred: ", str(e))
        return None


def get_user_student(student):
    try:
        user = User.query.get(student.ID)
        if user:
            return user
        else:
            return None
    except Exception as e:
        print("[user.get_user_student] Error occurred: ", str(e))
        return None


def get_all_users():
    try:
        users = User.query.all()
        if users:
            return users
        else:
            return []
    except Exception as e:
        print("[user.get_all_users] Error occurred: ", str(e))
        return []


def get_all_users_json():
    try:
        users = User.query.all()
        if not users:
            return []
        users = [user.get_json() for user in users]
        return users
    except Exception as e:
        print("[user.get_all_users_json] Error occurred: ", str(e))
        return []


def update_user_username(id, username):
    try:
        user = get_user(id)
        if user:
            user.username = username
            db.session.add(user)
            db.session.commit()
            return True
        return False
    except Exception as e:
        print("[user.update_user_username] Error occurred while updating username: ", str(e))
        db.session.rollback()
        return False


def update_username(userID, newUsername):
    try:
        user = get_user(userID)
        if user:
            user.username = newUsername
            db.session.commit()
            return True
        else:
            print("[user.update_username] Error: User not found.")
            return False
    except Exception as e:
        print("[user.update_username] Error occurred while updating username: ", str(e))
        db.session.rollback()
        return False


def update_name(userID, newFirstname, newLastName):
    try:
        user = get_user(userID)
        if user:
            user.firstname = newFirstname
            user.lastname = newLastName
            db.session.commit()
            return True
        else:
            print("[user.update_name] Error: User not found.")
            return False
    except Exception as e:
        print("[user.update_name] Error occurred while updating name: ", str(e))
        db.session.rollback()
        return False


def update_email(userID, newEmail):
    try:
        user = get_user(userID)
        if user:
            user.email = newEmail
            db.session.commit()
            return True
        else:
            print("[user.update_email] Error: User not found.")
            return False
    except Exception as e:
        print("[user.update_email] Error occurred while updating email: ", str(e))
        db.session.rollback()
        return False


def update_password(userID, newPassword):
    try:
        user = get_user(userID)
        if user:
            user.set_password(newPassword)
            db.session.commit()
            return True
        else:
            print("[user.update_password] Error: User not found.")
            return False
    except Exception as e:
        print("[user.update_password] Error occurred while updating password: ", str(e))
        db.session.rollback()
        return False


def update_faculty(userID, newFaculty):
    try:
        user = get_user(userID)
        if user:
            user.faculty = newFaculty
            db.session.commit()
            return True
        else:
            print("[user.update_faculty] Error: User not found.")
            return False
    except Exception as e:
        print("[user.update_faculty] Error occurred while updating faculty: ", str(e))
        db.session.rollback()
        return False
