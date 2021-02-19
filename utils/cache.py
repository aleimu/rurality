__doc__ = 'https://docs.djangoproject.com/zh-hans/3.0/topics/cache/'

# 1）导入缓存功能
from django.core.cache import cache  # 导入的cache就是配置的默认缓存
from django.core.cache import caches  # caches相当于全部缓存集
from django.views.decorators.cache import never_cache, cache_page, cache_control

def_cache = caches['default']
rds_cache = caches['redis']

assert def_cache == cache
assert rds_cache != cache
print('def_cache', def_cache)
print('rds_cache', rds_cache)
# 2）设置，如果将exp过期时间设置0或负值，就是删除缓存
# cache.set('key', 'value', exp=1000)
cache.set('key', 'value')
print(cache.set_many({'a': 1, 'b': 2, 'c': 3}))
print(cache.get_many(['a', 'b', 'c']))
# 3）获取
cache.get('key')
cache.set('num', 1)
cache.incr('num')
cache.incr('num', 10)
cache.decr('num')
cache.decr('num', 5)
cache.clear()


@cache_page(60 * 15, cache="redis")  # 可以选用缓存方式
@cache_page(60 * 15, key_prefix="site1")
@cache_control(max_age=3600)
@never_cache
def myview(request):
    pass


"""
https://segmentfault.com/q/1010000009705858
https://docs.djangoproject.com/zh-hans/3.0/topics/cache/#cache-key-prefixing

在设置的key字段前加前缀和版本号是django cache的机制, key由前缀，版本号，真正的key组成。
django在升级或者代码重构的时候有用，可以判断key是那个版本号，从而进行兼容.
"""
