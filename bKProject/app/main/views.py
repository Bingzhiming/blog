from . import main
from flask import render_template
from flask import session, request, make_response
from flask_login import login_required, current_user
from app.models import Permission
from app.decorator import permission_required
from .forms import EditUserForm
from app import db
from flask import redirect, url_for,abort
from .forms import BlogForm,CommentForm
from app.models import Blog,User,Comment,Collect
from wtforms.validators import ValidationError
from datetime import datetime,date

@main.route('/write_blog',methods=["GET","POST"])
@permission_required(Permission.WRITE)
def write_blog():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blog()
        blog.title = form.title.data
        blog.content = form.content.data
        blog.user=current_user
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template("main/write_blog.html",form = form)

@main.route('/follow')
@permission_required(Permission.FOLLOW)
def follow():
    user_id = request.args.get("user_id")
    if user_id is None:
        abort(404)
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    current_user.follow(user)
    return redirect(url_for('.user_main_page',user_id=user_id))

@main.route('/unfollow')
@permission_required(Permission.FOLLOW)
def unfollow():
    user_id = request.args.get("user_id")
    if user_id is None:
        abort(404)
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    current_user.unfollow(user)
    return redirect(url_for('.user_main_page',user_id=user_id))

@main.route('/comment',methods=["GET","POST"])
@permission_required(Permission.COMMENT)
def comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment()
        comment.content = form.content.data
        comment.user=current_user
        db.session.add(comment)
        db.session.commit()
        print(current_user.blogs)
        return redirect(url_for('.content',id=current_user.blogs.id))
    return render_template("main/comment.html",form=form)

@main.route('/blog_info')
@permission_required(Permission.READ)
def blog_info():
    blog_id = request.args.get("blog_id")
    if blog_id is None:
        abort(404)
    blog = Blog.query.get(blog_id)
    if blog is None:
        abort(404)
    return render_template("main/blog_info.html",b=blog)

@main.route('/edit_user',methods=["GET","POST"])
@login_required
def edit_user():
    form = EditUserForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        if len(form.password.data):
            current_user.password = form.password.data
        if len(form.label.data):
            current_user.label = form.label.data
        if len(form.location.data):
            current_user.location = form.location.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for("main.user_info"))
    form.name.data = current_user.name
    return render_template("main/edit_user.html",form=form)

@main.route('/index')
@permission_required(Permission.READ)
def index():
    page = request.args.get('page', type=int, default=1)
    pagination = Blog.query.order_by(Blog.id.desc()).paginate(page, 5, False)
    blogs = pagination.items
    b = Blog.query.all()
    t=date.today()
    d = Blog.query.filter(db.cast(Blog.time, db.DATE) == db.cast(t,db.DATE)).all()
    return render_template('main/index.html', pagination=pagination, blogs=blogs,b=len(b),d=len(d))

@main.route('/user_main_page')
def user_main_page():
    user_id=request.args.get("user_id")
    if user_id is None:
        abort(404)
    user=User.query.get(user_id)
    page = request.args.get("page",type=int,default=1)
    pagination = user.blogs.order_by(Blog.id.desc()).paginate(page, 5, False)
    return render_template('main/user_main_page.html', user=user, pagination=pagination)



@main.route('/user_info')
@login_required
def user_info():
    page = request.args.get("page",type=int,default=1)
    pagination = current_user.blogs.order_by(Blog.id.desc()).paginate(page, 5, False)
    return render_template("main/user_info.html",pagination=pagination)

@main.route('/collect')
@login_required
def collect():
    blog_id = request.args.get("blog_id")
    if blog_id is None:
        abort(404)
    blog = Blog.query.get(blog_id)
    if blog is None:
        abort(404)
    current_user.collect_blog(blog_id)
    return redirect(url_for('.blog_info',blog_id=blog_id))

@main.route('/mycollect')
@login_required
def mycollect():
    page = request.args.get('page', type=int, default=1)
    pagination  = current_user.collects.order_by(Collect.id.desc()).paginate(page, 5, False)
    collects = pagination.items
    c=Collect.query.filter_by(collector_id=current_user.id).all()
    for  i in c:
        print(i.id,i.blog_id)
    return render_template("main/collect.html",collects=collects,pagination=pagination)
