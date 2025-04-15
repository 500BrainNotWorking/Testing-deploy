from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from sqlalchemy.exc import SQLAlchemyError

from App.models import User

def jwt_authenticate(username, password):
    try:
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return create_access_token(identity=username)
    except SQLAlchemyError as e:
        print(f"[DB ERROR] jwt_authenticate: {e}")
    return None

def login(username, password):
    try:
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
    except SQLAlchemyError as e:
        print(f"[DB ERROR] login: {e}")
    return None

def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        try:
            return User.query.get(id)
        except SQLAlchemyError as e:
            print(f"[DB ERROR] load_user: {e}")
            return None

    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        try:
            user = User.query.filter_by(username=identity).one_or_none()
            if user:
                return user.ID
        except SQLAlchemyError as e:
            print(f"[DB ERROR] user_identity_lookup: {e}")
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        try:
            identity = jwt_data["sub"]
            return User.query.get(identity)
        except SQLAlchemyError as e:
            print(f"[DB ERROR] user_lookup_callback: {e}")
            return None

    return jwt
