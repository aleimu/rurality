__doc__ = "对django的特性测试"

from base.api import *
import logging
from pprint import pprint
from django.conf import settings
import asyncio

logger = logging.getLogger('info')


class HealthApi(BaseApi):
    NEED_LOGIN = False

    need_params = {
    }

    def get(self, request, params):
        # TODO: 检查所需组件的可访问状态
        # mysql、redis等
        return 'ok'


# 简单的示例
class ExploreApi(BaseApi):
    NEED_LOGIN = False

    need_params = {
    }

    def get(self, request, params):
        # pprint(request.META)
        # pprint(vars(request))
        # logger.info("--------%s-----" % vars(request))
        # return vars(request)
        # pprint(vars(settings))
        # return vars(settings)
        pprint(request._start_time)
        # raise Exception('for test!')
        return 'ok'


# 类式视图,无法简单使用
class AsyncApi(BaseApi):
    """尝试下异步asyncio"""
    NEED_LOGIN = False

    need_params = {
    }

    async def get(self, request, params):
        pprint(request._start_time)
        return self._processing_something(request)

    async def _processing_something(self, request: HttpRequest):
        """处理一些耗时任务"""
        await asyncio.sleep(10)
        return 'ok'

    async def put(self, request, params):
        pprint(request._start_time)
        return "ok"


# 很老的使用协程的方式...没有FastApi那么优雅
class AsyncLoopApi(BaseApi):
    """在视图函数内构建协程所需的事件循环"""
    NEED_LOGIN = False

    need_params = {
    }

    def get(self, request, *args, **kwargs):
        start = time.time()
        count = 10
        # 创建一个新的事件循环
        loop = asyncio.new_event_loop()
        # 将 loop 设置为当前 OS 线程的当前事件循环。
        asyncio.set_event_loop(loop)
        self.loop = loop
        try:
            # 将任务对象注册到事件循环队列中并且开启了事件循环
            results = loop.run_until_complete(self.gather_tasks(list(range(count))))
        finally:
            loop.close()
        print(results)  # 返回给json序列化时不可以是协程对象,而是协程的最后结果
        end = time.time()
        return {"code": 200, "count": len(results), "msg": "获取数据成功", "time": end - start}

    async def gather_tasks(self, limit_list):
        # 创建task任务
        task = (self.select_data(self.current_sql, item) for item in limit_list)
        # 接受task任务
        results = await asyncio.gather(*task)
        return results

    async def select_data(self, func, *args):
        # 可以是  ThreadPoolExecutor / ProcessPool  , 如果是None 则使用默认线程池
        future = self.loop.run_in_executor(None, func, *args)
        response = await future
        return response

    def current_sql(self, size_list):
        # Lock.acquire()
        # with connection.cursor() as cursor:
        #     # 此处对于分页查询，进行优化 where id > xxx 可以缩小范围
        #     res = cursor.execute("INSERT INTO api_data (name) VALUES({})".format(size_list))
        res = None
        asyncio.sleep(2)
        return res


# 异步模板
class MyAsyncView(BaseApi):
    """尝试了半天也没发现Django对view class的异步支持,这里按上面的方式实现下简单的异步处理,以便做测试"""
    NEED_LOGIN = False

    need_params = {
    }

    # async def get(self, request, *args, **kwargs) 这种形式是不支持的,除非在外层将coroutine对象再解析出来,一般不建议.
    # 起10个耗时5秒的协程,总共只耗时5秒
    def get(self, request, *args, **kwargs):
        start = time.time()
        count = 10
        # 创建一个新的事件循环
        loop = asyncio.new_event_loop()
        # 将 loop 设置为当前 OS 线程的当前事件循环。
        asyncio.set_event_loop(loop)
        self.loop = loop
        try:
            # 初始化异步任务列表
            futus = asyncio.gather(*[self.work(x) for x in range(count)])
            # 将任务对象注册到事件循环队列中并且开启了事件循环
            results = loop.run_until_complete(futus)
        finally:
            loop.close()
        end = time.time()
        # 返回给json序列化时不可以是协程对象,而是协程的最后结果
        return {"code": 200, "count": sum(results), "msg": "获取数据成功", "time": end - start}

    async def work(self, x):
        """模拟耗时的异步任务"""
        logging.info(f'Waiting :{str(x)}')
        await asyncio.sleep(5)
        logging.info(f'Done :{str(x)}')
        return x


# TODO 封装一个BaseAsyncApi
# 既然异步,那就全称异步,这就是异步的传染性!
# Django3.1版本中的ORM、缓存层和其他执行长时间网络调用的代码还暂时不支持异步访问


# 函数式视图,可以正常使用
async def test(request):
    t0 = time.time()
    await asyncio.sleep(5)
    await asyncio.sleep(5)
    pprint(time.time() - t0)  # 10秒
    return HttpResponse('Hello, async world!')


# 同步函数视图
def test0(request):
    time.sleep(5)
    return HttpResponse('测试-同步')


# 可以看到上面那种在视图中建立事件循环并处理的视图的方式方式有点复杂,对于简单的请求可以尝试下面的装饰器
from asgiref.sync import sync_to_async, async_to_sync  # 同步转异步,异步转同步


# results = sync_to_async(Blog.objects.get)(pk=123)
# 注意圆括号，千万不要写成results = sync_to_async(Blog.objects.get(pk=123))

# 同步转异步
@sync_to_async
def test1(request):
    time.sleep(5)
    return HttpResponse('测试-同步转异步')


# 异步转同步
@async_to_sync
async def test2(request):
    await asyncio.sleep(5)
    return HttpResponse('测试-异步转同步')


# 同步转异步
@sync_to_async
def test3(request):
    """尝试"""
    # return HttpResponse(sum([work(x) for x in range(10)]))
    return HttpResponse(work(1))


@sync_to_async
def work(x):
    """模拟耗时的异步任务"""
    logging.info(f'Waiting :{str(x)}')
    time.sleep(1)
    logging.info(f'Done :{str(x)}')
    return x


"""
# https://docs.djangoproject.com/zh-hans/3.0/topics/async/
sync_to_async() 有两种线程模式：
thread_sensitive=False (默认)：同步函数将在一个全新的线程中运行，该线程一旦完成，将会关闭。
thread_sensitive=True: 同步函数将与所有其它 thread_sensitive=True的 函数在相同线程里运行，这个线程通常就是主线程。
"""
