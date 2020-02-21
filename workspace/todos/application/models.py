from application import db

class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)

    completed = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.String(), nullable=False)
    
    def __repr__(self):
        return f'<Todo id={self.id} completed={self.completed} description={self.description}>'