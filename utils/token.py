__doc__ = "简单的token操作"

import traceback
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated

from django.http import HttpResponse

from utils.cache import rds_cache as rds

expire = 3000


# session方式,暂时不用
def get_session(request):
    if request.session.has_key('username'):
        username = request.session['username']
        print(username)  # SR
        return HttpResponse(username)


def set_session(request):
    request.session['username'] = 'SR'
    request.session['age'] = 18
    request.session.set_expiry(50)  # 0:表示关闭浏览器过期；None:表示永不过期。 默认两周后过期。
    return HttpResponse('设置session')


class TokenAuth(BaseAuthentication):
    """token校验的中间件"""

    def authenticate(self, request):
        token = request.GET.get("token")
        if Token.check(token):
            return
        else:
            raise NotAuthenticated("你没有登入")


class Permisson(BasePermission):  # 写一个类继承 BasePermission
    def has_permission(self, request, view):  # 函数名字不能变，从继承的BasePermission类里找函数名
        if request.user.type == 3:  # 权限开始认证,认证组件通过已将用户赋值给 request.user
            print("权限认证通过")
            return True  # 权限认证通过返回True
        else:
            print("权限认证失败")
            return False  # 权限认证没通过返回False


class Token:
    """对token做一层简单的封装,此处主要是用redis存储token和用户信息"""
    expire = 3600

    @staticmethod
    def source(request):
        """约定token的参数都来自url的查询字符串token"""
        token = request.GET.get('token')  # django并没有提供获取全局request的方法,所以此处的request和view里的不是一个.
        return token

    @staticmethod
    def create(name):
        """token的格式"""
        token = name
        return token

    @staticmethod
    def get(name):
        """查询token的内容"""
        try:
            # store_token = rds.hgetall(name)   # 还不支持redis的常用API,只有些简单的API...
            store_token = rds.get(name)
            if not store_token:
                return False
            else:
                return store_token
        except:
            traceback.print_exc()
            return False

    @staticmethod
    def check(token):
        """检查token是否存在-有效"""
        try:
            token = rds.has_key(token)
            if token:
                return True
        except:
            traceback.print_exc()
        return False

    @staticmethod
    def flush(token):
        """刷新token有效期"""
        rds.expire(token, expire)

    @staticmethod
    def store(token, info):
        """存储token到redis"""
        rds.set(token, info, expire)
        return token

    @staticmethod
    def delete(token):
        """删除token"""
        rds.delete(token)
