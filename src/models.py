from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    task_relationship = db.relationship('Task', lazy=True)

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user_name,
            # "task":self.task_relationship
            # do not serialize the password, its a security breach
        }
   
    def get_all_users():
        users = User.query.all()
        all_users = list(map(lambda x: x.serialize(), users))
        return all_users

    @classmethod
    def get_user(cls,  username):
        user  = User.query.filter_by(user_name= username)
        all_users = list(map(lambda x: x.serialize(), user))
        return all_users
    
    def delete_user(username):
        Task.delete_task(username)
        user = User.query.filter_by(user_name= username)
        user.delete()
        db.session.commit()
        return username

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(255), unique=False, nullable=False)
    done = db.Column(db.Boolean(False), unique=False, nullable=False)
    user_to_do = db.Column(db.String(80), db.ForeignKey("user.user_name"), nullable=False)
    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    # def __repr__(self):
    #     return f"task: {self.label}, done:{self.done}"

    def add_task(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "user_to_do":self.user_to_do,
            "label": self.label,
            "done":self.done
            # do not serialize the password, its a security breach
        }
    @classmethod
    def get_user_tasks(cls, username):
        tasks  = Task.query.filter_by(user_to_do= username)
        all_tasks = list(map(lambda x: x.serialize(), tasks))
        return all_tasks

    def update_task(self, username, taskName, isDone, id):
        task = Task.query.filter_by(user_to_do= username, label = taskName, id = id).first()
        task.done = isDone
        db.session.commit()

    def delete_task(username):
        user = Task.query.filter_by(user_to_do= username)
        user.delete()
        db.session.commit()
    


    