from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, DataRequired, Regexp, EqualTo
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from app.models import User
from wtforms.validators import ValidationError

class ActiveEmailForm(FlaskForm):
    email = StringField(label="邮箱",validators=[DataRequired(message="邮箱必须添加"),Length(1,64,message="长度必须在1-64位之间"),Email(message="必须是邮箱格式")])
    submit = SubmitField(label="重新发送邮件")

    def validate_email(self,field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError("此用户不存在")
        if user.confirmed:
            raise ValidationError("此用户已经激活")

class LoginForm(FlaskForm):
    email = StringField(label="邮箱",validators=[DataRequired(message="邮箱必须添加"),Length(1,64,message="长度必须在1-64位之间"),Email(message="必须是邮箱格式")])
    password = PasswordField(label="密码",validators=[DataRequired(message="密码必须填写"),Length(6,32,message="长度必须6-32位之间")])
    remember_me = BooleanField(label="记住密码",default=False)
    submit = SubmitField(label="登录")

    def validate_email(self,field):
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            raise ValidationError("此用户不存在")
        if not user.confirmed:
            raise ValidationError("此用户未激活")

class RegisterForm(FlaskForm):
    email = StringField(label="邮箱",validators=[DataRequired(message="邮箱必须添加"),Length(1,64,message="长度必须在1-64位之间"),Email(message="必须是邮箱格式")])
    name = StringField(label="昵称",validators=[DataRequired(message="昵称必须输入"),Length(1,32,message="长度必须在1-32位之间")])
    password = PasswordField(label="密码",validators=[DataRequired(message="密码必须填写"),Length(6,32,message="长度必须6-32位之间"),Regexp('^.*$', 0, message='密码必须包含xxx')])
    password_again = PasswordField(label="确认密码",validators=[EqualTo("password",message="两次输入密码不一致")])
    submit = SubmitField(label="注册")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user :
            raise ValidationError('此邮箱已经被注册')

    def validate_name(self, field):
        user = User.query.filter_by(name=field.data).first()
        if user:
            raise ValidationError("昵称已被注册")