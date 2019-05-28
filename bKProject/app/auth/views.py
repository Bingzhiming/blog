from . import auth
from flask import request,session,make_response,render_template
from .forms import LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required
from flask import redirect, url_for
from flask_login import current_user
from .forms import RegisterForm
from app import db
from flask import flash
from app.email import send_mail
from flask import current_app, abort
from .forms import ActiveEmailForm
from app.models import Role

@auth.route('/confirm', methods=['GET','POST'])
def confirm() :
    form = ActiveEmailForm()
    if form.validate_on_submit() :
        user = User.query.filter_by(email=form.email.data).first()
        temp = render_template('email/register_email.html', name=user.name, token=user.generate_token())
        send_mail('注册邮件', current_app.config['MAIL_USERNAME'], [user.email], None, temp)
        # return redirect(url_for('.login'))
        email = user.email
        email_addr = 'mail.' + email[email.index('@') + 1:]
        return render_template('auth/active.html', user=user, email_addr=email_addr)
    token = request.args.get('token')
    if User.check_token(token):
        return redirect(url_for('main.user_info'))
    else :
        return render_template('auth/reactive.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register() :
    form = RegisterForm()
    if form.validate_on_submit() :
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.password = form.password.data
        user.role = Role.query.filter_by(default=True).first()
        db.session.add(user)
        db.session.commit()
        flash('恭喜《'+user.name+'》注册成功！' + '请登录！')
        #发邮件
        temp = render_template('email/register_email.html', name=user.name, token=user.generate_token())
        send_mail('注册邮件', current_app.config['MAIL_USERNAME'],[user.email], None, temp)
        #return redirect(url_for('.login'))
        email = user.email
        email_addr = 'mail.' + email[email.index('@') + 1:]


        return render_template('auth/active.html', user=user, email_addr=email_addr)
    return render_template('auth/register.html', form=form)

# http://127.0.0.1:5000/auth/confirm?id=sdfjkasfjfjsjfjfjfaj;afs

@auth.route('/logout')
@login_required
def logout() :
    logout_user()
    return redirect(url_for('.login'))

# 127.0.0.1:5000/auth/login
@auth.route('/login', methods=['GET','POST'])
def login() :
    form = LoginForm()
    if form.validate_on_submit() :
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) :
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        else :
            form.password.errors.append('密码有误')


    return render_template('auth/login.html', form=form)

@auth.route('/unconfirm')
def unconfirm() :
    email = request.args.get('email')
    if email is None :
        abort(404)
    user = User.query.filter_by(email=email).first()
    if user is None :
        abort(404)
    email = user.email
    email_addr = 'mail.'+email[email.index('@')+1:]
    return render_template('auth/active.html', user=user, email_addr=email_addr)

@auth.before_app_request
def before_goto_view():
    if current_user.is_authenticated:
        current_user.update_last_time()
