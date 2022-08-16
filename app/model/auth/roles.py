from app import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name_role = db.Column(db.String(50), unique=True)
   
    def __repr__(self):
        return '<Role {}>'.format(self.name)
        
    def to_dict(self):
        return {
            'name_role': self.name_role
        }