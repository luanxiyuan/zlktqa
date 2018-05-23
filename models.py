#encoding: utf-8
from datetime import datetime
from exts import db


class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Question(db.Model):
    __tablename__ = 't_question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    #now()获取的是服务器第一次运行的时间
    #now是每次创建一个模型的时候都获取当前时间
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('t_user.id'))

    author = db.relationship('User', backref=db.backref('questions'))


class Comment(db.Model):
    __tablename__ = 't_comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('t_question.id'))

    author = db.relationship('User', backref=db.backref('comments'))
    question = db.relationship('Question', backref=db.backref('comments', order_by=create_time.desc()))