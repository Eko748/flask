from functools import wraps
from multiprocessing import current_process
from tabnanny import check
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='1122')
    username = db.Column(db.String(100), nullable=False, server_default='')
    roles = db.relationship('Role', secondary='user_roles')
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # def is_active(self):
    #     """True, as all users are active."""
    #     return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email
    
    def get_emp(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        self.level == "EMPLOYEE"
        return self.level

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    def __repr__(self):
        return '<User {}>'.format(self.name)
    
    def to_dict(self):
        return {
            'username': self.username,
            'is_active': self.active,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def setPassword(self,password):
        self.password = generate_password_hash(password)
        
    def checkPassword(self,password):
        return check_password_hash(self.password, password)