from application import db

class Role(db.Model):
    # Flask will use the lower-case of class name as default table name
    __tablename__ = 'roles'    
    
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(64), unique=True)
    # relationship -- object-level description    
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):        
        return '<Role {}>'.format(self.name)

class User(db.Model):
    # Flask will use the lower-case of class name as default table name    
    __tablename__ = 'users'    
    
    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String(64), nullable=False, index=True)
    # relationship -- table-level description    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):        
        return '<User {}>'.format(self.username) 