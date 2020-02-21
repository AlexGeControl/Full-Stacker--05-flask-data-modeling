from application import db

class TodoList(db.Model):
    __tablename__ = 'todolists'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False, default='Uncategorized')

    todos = db.relationship('Todo', backref='todolist', lazy=True)

    def __repr__(self):
        return f'<TodoList name={self.name}>'

class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)

    completed = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.String(), nullable=False)
    
    todolist_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=True)

    def __repr__(self):
        return f'<Todo description={self.description} completed={self.completed}>'
    
    def to_dict(self):
        data = {
            "id": self.id,
            "completed": self.completed,
            "description": self.description
        }

        return data