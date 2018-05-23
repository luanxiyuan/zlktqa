#encoding: utf-8
import os

DEBUG = True
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = "mysql://root:admin@127.0.0.1:3306/zlktqa?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False