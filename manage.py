#encoding: utf-8

from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from app import app
from exts import db
from models import User, Question

manager = Manager(app)

# 使用migrate需要绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本命令到manager中
manager.add_command('db', MigrateCommand)


@manager.command
def create_tables():
    db.create_all()


if __name__ == '__main__':
    manager.run()