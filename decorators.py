#encoding: utf-8
from functools import wraps
from flask import session, redirect, url_for


#登录限制的装饰器
#装饰器实际上就是一个函数，但有两个特别之处：
#1. 参数是一个函数
#2. 返回值是一个函数
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            print('没有登录，请先登陆')
            return redirect(url_for('login'))
    return wrapper