from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, DataRequired, Regexp, EqualTo
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from app.models import User
from wtforms.validators import ValidationError
from flask import render_template
from wtforms import TextAreaField

class BlogForm(FlaskForm) :
    title = StringField(label='标题', validators=[
        DataRequired(message='标题必须填写'),
        Length(1, 32, message='长度必须是1-32')
    ])
    content = TextAreaField(label='正文', validators=[
        DataRequired(message='正文必须填写'),
        Length(20, 1024, message='长度必须是20-1024')
    ])
    submit = SubmitField(label='提交')

class CommentForm(FlaskForm) :
    content = TextAreaField(label='评论',validators=[
        Length(1, 200, message='长度必须是0-200')
    ])
    submit = SubmitField(label='发表')

class EditUserForm(FlaskForm) :
    name = StringField(label='昵称', validators=[
        DataRequired(message='必须填写昵称'),
        Length(1, 64, message='长度必须是1-64'),
    ])
    label= StringField(label='个性签名', validators=[
        Length(0, 128, message='长度必须是0-128')
    ])
    location = StringField(label='位置', validators=[])

    password = PasswordField(label='密码', validators=[
        Length(0, 64, message='长须必须是6-64'),
        Regexp('^.*$', 0, message='密码必须包含xxx')
    ])
    password_again = PasswordField(label='确认密码', validators=[
        EqualTo('password', message='两次输入密码不一致')
    ])
    submit = SubmitField(label='确认修改')

    #自定义校验方法
    def validate_name(self, field):
        if field.data == 'lizhiyong' :
            # 异常信息会被放到name的errors中
            raise ValidationError('你没资格用这个名字')