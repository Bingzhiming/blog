from functools import wraps
from flask_login import current_user
from flask import abort

# 有问题  permission_required这个特装饰器以来login_required
# def permission_required(permission) :
#     def check_permission(fun) :
#         @wraps(fun)
#         def func() :
#             if current_user.role.permission & permission != permission :
#                 abort(403)
#             return fun()
#         return func
#     return check_permission

# 权限：
# 视图函数都要用权限装饰器去装饰
# 登录用户：角色 每一种角色都有不同的权限
# 匿名用户：可以有权限，但一般没有权限

def permission_required(permission) :
    def check_permission(fun) :
        @wraps(fun)
        def func() :
            if not current_user.has_permission(permission):
                abort(403)
            return fun()
        return func
    return check_permission

def admin_required(fun) :
    @wraps(fun)
    def func() :
        if not current_user.is_admin() :
            abort(403)
        return fun()
    return func

def moderator_required(fun) :
    @wraps(fun)
    def func() :
        if not current_user.is_moderator() :
            abort(403)
        return fun()
    return func

