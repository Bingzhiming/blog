import pymysql
pymysql.install_as_MySQLdb()
from app import create_app
from app import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app('develop')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

from app.models import User,Role
@manager.command
def init() :
    Role.create_roles()
    User.create_super_user()

manager.run()