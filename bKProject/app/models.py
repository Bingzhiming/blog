from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import login_user

from datetime import datetime

class Permission() :
    READ = 0x00
    FOLLOW = 0x01
    WRITE = 0x02
    COMMENT = 0x04
    MANAGER_COMMENT = 0x08
    ADMIN = 0x80

class Role(db.Model) :
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    permission = db.Column(db.Integer)
    default = db.Column(db.Boolean, default=False)

    users = db.relationship('User',lazy='dynamic', backref='role', cascade='all, delete-orphan')

    @staticmethod
    def create_roles():
        roles = {
            'user':[Permission.FOLLOW | Permission.WRITE | Permission.COMMENT, True],
            'moderator':[Permission.MANAGER_COMMENT, False],
            'admin':[0xff, False]
        }
        for name in roles :
            role = Role.query.filter_by(name=name).first()
            if role is None :
                role=Role()
            role.name = name
            role.permission = roles[name][0]
            role.default = roles[name][1]
            db.session.add(role)
        db.session.commit()

# user = User()
# user.password
# user.password = '12345'

class Follow(db.Model):
    __tablename__="follows"
    fensi_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    dav_id=db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    time=db.Column(db.DateTime,default=datetime.now)



class User(db.Model, UserMixin) :
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64))

    confirmed = db.Column(db.Boolean, default=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))

    def __str__(self):
        return self.name + ' ' + str(self.id)

    @property
    def password(self):
        raise AttributeError('密码不可读取')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create_super_user():
        user = User()
        user.email = 'lizhiyong_python@163.com'
        user.password = '123456'
        user.name = 'lizhiyong'
        user.confirmed = True
        user.role = Role.query.filter_by(name='admin').first()
        db.session.add(user)
        db.session.commit()

    # 生成token
    def generate_token(self):
        serializer = Serializer(current_app.config['SECRET_KEY'], 60*2)
        token = serializer.dumps({'user_id':self.id})
        return token

    # 解密token
    @staticmethod
    def check_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try :
            data = serializer.loads(token)
        except :
            return False

        id = data.get('user_id')
        if id is None :
            return False
        user = User.query.get(id)
        if user is None :
            return False
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return True

    def has_permission(self, permission):
        return self.role.permission & permission == permission

    def is_admin(self):
        return self.role.permission == 0xff

    def is_moderator(self):
        return self.role.permission == Permission.MANAGER_COMMENT

    label = db.Column(db.String(128), default='这个人很懒，什么都没留下')
    location = db.Column(db.String(32), default='火星')

    blogs = db.relationship('Blog', lazy='dynamic', backref='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', lazy='dynamic', backref='user', cascade='all, delete-orphan')
    collects = db.relationship('Collect', backref='user', lazy='dynamic')

    register_time = db.Column(db.DateTime, default=datetime.now)
    login_time = db.Column(db.DateTime, default=datetime.now)
    last_time = db.Column(db.DateTime, default=datetime.now)

    fensis = db.relationship('Follow', foreign_keys=[Follow.dav_id],
                             backref=db.backref('dav'), lazy='dynamic',
                             cascade='all,delete-orphan')
    davs = db.relationship('Follow', foreign_keys=[Follow.fensi_id],
                           backref=db.backref('fensi'), lazy='dynamic',
                           cascade='all,delete-orphan')

    def update_login_time(self):
        self.login_time = datetime.now()
        db.session.add(self)
        db.session.commit()

    def update_last_time(self):
        self.last_time = datetime.now()
        db.session.add(self)
        db.session.commit()

    def is_fensi_of(self,user):
        if self.davs.filter_by(dav_id=user.id).first():
            return True
        return False

    def is_dav_of(self,user):
        if self.fensis.filter_by(fensi_id=user.id).first():
            return True
        return False

    def follow(self,user):
        if not self.is_fensi_of(user):
            follow = Follow()
            follow.fensi = self
            follow.dav = user
            db.session.add(follow)
            db.session.commit()

    def unfollow(self,user):
        if self.is_dav_of(user):
            follow = self.davs.filter_by(dav_id = user.id).first()
            db.session.delete(follow)
            db.session.commit()

    def collect_blog(self, blog_id):
        cb = Collect()
        cb.blog_id = blog_id
        cb.user = self
        db.session.add(cb)
        db.session.commit()

#current_user是一个代理
#如果用户登录了，那么current_user代表当前用户的user对象
#如果用户没有登录，那么current_user代表AnonymouseUser类型的对象
#构建一个匿名用户类  匿名用户类需要指定 __init__.py login_manager.anonymous_user = xxxx
from flask_login import AnonymousUserMixin
class AnonymousUser(AnonymousUserMixin) :
    name = '游客'
    permission = Permission.READ
    def has_permission(self, permission):
        return self.permission & permission == permission

    def is_admin(self):
        return False

    def is_moderator(self):
        return False

class Blog(db.Model) :
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    comments = db.relationship('Comment',lazy='dynamic', backref='blog', cascade='all, delete-orphan')


class Collect(db.Model):
    __tablename__="collects"
    id = db.Column(db.Integer,primary_key=True)
    collector_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='CASCADE'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id', ondelete='CASCADE'))
    time = db.Column(db.DateTime, default=datetime.now)

class Comment(db.Model) :
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.now)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))



from app import login_manager
@login_manager.user_loader
def load_user(id) :
    return User.query.filter_by(id=int(id)).first()
