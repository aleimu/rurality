__doc__ = "常用中间件"

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

"""
在请求视图被处理前，中间件由上至下依次执行
在请求视图被处理后，中间件由下至上依次执行

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 以上为django自带的7种中间件,如下为自定义的
    'util.middle.Mymd1',
    'util.middle.Mymd2',
]
"""



class Mymd1(MiddlewareMixin):
    """
    # 可以自定义的5个阶段的中间件方法:
    这些方法的返回值可以是None或一个HttpResponse对象，
    如果是None，则继续按照django定义的规则向后继续执行，
    如果是HttpResponse对象，则直接将该对象返回给用户

    # 总结:
     - 当配置多个中间件时，会按照MIDDLEWARE中的注册顺序，也就是列表的索引值，从前到后依次执行的。
     - 不同中间件之间传递的request都是同一个对象
    """

    def process_request(self, request):
        """
        中间件的process_request方法是在执行视图函数之前执行的。
        请求来的时候会按照配置文件中注册的中间件从上往下的顺序依次执行每一个中间件里面process_request方法
        """
        print('我是第一个自定义中间件里面的process_request方法')
        # return HttpResponse("我是第一个中间件返回的Httpresponse对象")

    def process_response(self, request, response):
        """
        响应走的时候会按照配置文件中注册的中间件从下往上的顺序依次执行每一个中间件里面的process_response方法
        """
        print('我是第一个中间件里面的process_reponse方法')
        return response  # 就是后端返回给前端浏览器的响应数据

    def process_view(self, request, view_func, *args, **kwargs):
        """
        路由匹配成功执行视图函数之前触发
        """
        print(view_func, args, kwargs)
        print('我是第一个中间件里面的process_view')

    def process_template_response(self, request, response):
        """
        视图函数返回的对象中必须要有render属性对应的render方法
        """
        print('我是第一个中间件里面的process_template_reponse方法')
        return response

    def process_exception(self, request, exception):
        """
        当视图函数报错的时候自动触发
        """
        print('exception:', exception)
        print('我是第一个中间件里面的process_exception')


class Mymd2(MiddlewareMixin):
    def process_request(self, request):
        print('我是第二个自定义中间件里面的process_request方法')

    def process_response(self, request, response):
        print('我是第二个中间件里面的process_reponse方法')
        return response

    def process_view(self, request, view_func, *args, **kwargs):
        print(view_func, args, kwargs)
        print('我是第二个中间件里面的process_view')

    def process_template_response(self, request, response):
        print('我是第二个中间件里面的process_template_reponse方法')
        return response

    def process_exception(self, request, exception):
        print('exception:', exception)
        print('我是第二个中间件里面的process_exception')


class Middleware:
    def __init__(self, get_response=None):
        pass

    def process_request(self, request):
        # 在每个请求上，request对象产生之后，URL地址匹配之前进行调用，返回None或者Httpresponse对象
        pass

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # 在处理视图之前，在每个请求上，URL地址匹配之后，视图函数调用之前，返回的是None或Httpresponse对象
        pass

    def process_response(self, request, response):
        # 处理响应后，视图函数调用之后，所有的响应在返回浏览器之前被调用，在每一个请求上调用，返回                HTTPresponse对象
        pass

    def process_exception(self, request, exception):
        # 异常处理：当视图抛出异常时调用，在每一个请求上调用，返回的Httpresponse对象
        pass
