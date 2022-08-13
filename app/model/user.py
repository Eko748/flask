from tabnanny import check
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(60), index=True, unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    level = db.Column(db.BigInteger, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.name)
    
    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'level': self.level,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def setPassword(self,password):
        self.password = generate_password_hash(password)
        
    def checkPassword(self,password):
        return check_password_hash(self.password, password)