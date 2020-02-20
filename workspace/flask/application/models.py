from application import db

class Role(db.Model):
    # Flask will use the lower-case of class name as default table name
    __tablename__ = 'roles'    
    
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(64), unique=True)    
    
    def __repr__(self):        
        return '<Role {}}>'.format(self.name)

class User(db.Model):
    # Flask will use the lower-case of class name as default table name    
    __tablename__ = 'users'    
    
    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String(64), unique=True, index=True)    
    
    def __repr__(self):        
        return '<User {}>'.format(self.username) 