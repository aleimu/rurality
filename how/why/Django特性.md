# 记录一些Django框架的特性,会和Flask做一些对比学习

# Todo

- 将之前整理的合并过来
- 尝试改变一些组件功能


![异步视图](https://docs.djangoproject.com/zh-hans/3.0/topics/async/)
![请求处理流程](https://blog.csdn.net/bingjia103126/article/details/105466669)
![请求处理流程](https://img-blog.csdnimg.cn/20200412115544581.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpbmdqaWExMDMxMjY=,size_16,color_FFFFFF,t_70)
![django请求处理流程](https://images2018.cnblogs.com/blog/867021/201804/867021-20180409234112982-196913305.png)
![中间件处理流程](https://images2018.cnblogs.com/blog/867021/201804/867021-20180409214356226-286908304.png)
![中间件处理流程2](https://images2018.cnblogs.com/blog/867021/201804/867021-20180409214433968-2137571775.png)

# settings的懒加载

django 中使用 LazyObject 代理类。加载函数是 _setup 函数，当获取属性时才会去加载。


- WSGI：全称是Web Server Gateway Interface，是一种规范，只适用于Python语言。要实现WSGI协议，必须同时实现web server和web
application，当前运行在WSGI协议之上的web框架有Bottle, Flask, Django。 
- uwsgi：与WSGI一样是一种通信协议，是uWSGI服务器的独占协议，用于定义传输信息的类型(type of
information)，每一个uwsgi packet前4byte为传输信息类型的描述，与WSGI协议是两种东西，据说该协议是fcgi协议的10倍快。 
- uWSGI：是一个web服务器，实现了WSGI协议、uwsgi协议、http协议等。

Web服务器可分为WSGI和ASGI两种模式，在不同的模式下，同步和异步视图有性能差别：

    WSGI+同步视图：传统模式
    ASGI+异步视图：性能最佳的异步模式
    WSGI+同步视图+异步视图：传统模式混杂异步，异步视图的性能不能正常发挥
    ASGI+同步视图+异步视图：异步模式混杂传统视图，异步性能最佳

# 总的来说,Django的写起异步视图还不完善,远没有FastApi等异步框架写起来丝滑,更没有go等原生支持异步的语言方便.