#encoding: utf-8
from flask import Flask, render_template, request, session, redirect, url_for
from exts import db
import config
import pymysql
from models import User, Question, Comment
from decorators import login_required
import logging, os, time

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

#log配置，实现日志自动按月生成文件夹，并按照日期生成日志文件
def make_dir(make_dir_path):
    path = make_dir_path.strip()
    if not os.path.exists(path):
        os.makedirs(path)
    return path
log_dir_name = "logs"
log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
log_file_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + os.sep + log_dir_name
make_dir(log_file_folder)
log_file_str = log_file_folder + os.sep + log_file_name
log_level = logging.WARNING

handler = logging.FileHandler(log_file_str, encoding='UTF-8')
handler.setLevel(log_level)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)


@app.route('/')
def index():
    app.logger.error('这是第一个erro log')
    questions = db.session.query(Question).order_by(Question.create_time.desc()).all()
    return render_template('index.html', questions = questions)


#登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = db.session.query(User).filter_by(telephone=telephone, password=password).first()
        if user:
            if user.password == password:
                session['user_id'] = user.id
                #如果想在31天之内不需要登陆
                session.permanent = True
                return redirect(url_for('index'))
            else:
                return u'密码输入错误，请重新输入'
        else:
            return u'该手机号未注册，请先注册'


@app.route('/logout')
def logout():
    # session.pop('user_id')
    session.clear()
    return redirect(url_for('index'))


#注册
@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')

        user = db.session.query(User).filter_by(telephone = telephone).first()
        if user:
            return u'该手机号已经被注册'
        elif repassword != password:
            return u'两次输入的密码不一致'
        else:
            new_user = User(telephone=telephone, username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/raise_question', methods=['GET', 'POST'])
@login_required
def raise_question():
    if request.method == 'GET':
        return render_template('raise_question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        new_question = Question(title=title, content=content, author_id=session.get('user_id'))
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/question/<id>')
@login_required
def question(id):
    question = db.session.query(Question).filter_by(id=id).first()
    if question:
        # comments = db.session.query(Comment).filter_by(question=question).order_by(Comment.create_time.desc()).all()
        return render_template('question.html', question=question)
    else:
        return u'该问题不翼而飞了'


@app.route('/add_comment/<question_id>', methods=['POST'])
@login_required
def add_comment(question_id):
    content = request.form.get('content')
    user_id = session.get('user_id')
    comment = Comment(content=content, author_id=user_id, question_id=question_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('question', id=question_id))


#上下文处理器钩子函数，返回字典数据会被当成模板数据渲染
#上下文处理器返回的数据，在所有页面中都是可用的
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
