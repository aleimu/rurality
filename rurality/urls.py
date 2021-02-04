from django.urls import path
from django.urls import include

from rurality.apis import HealthApi, ExploreApi, AsyncApi, test, test0, test1, test2, test3, MyAsyncView

urlpatterns = [
    path('api/v1/', include({
        path('account/', include('account.urls')),
        path('business/', include('business.urls')),
        path('asset/', include('asset.urls')),
        path('scheduler/', include('scheduler.urls')),
        path('component/', include('component.urls')),
    })),
    path('health/', HealthApi.as_view()),
    path('test/', ExploreApi.as_view()),  # 特性测试

    path('async/async/', AsyncApi.as_view()),  # 异步特性测试
    path('async/my/', MyAsyncView.as_view()),  # 异步特性测试

    path('async/t', test),  # 同步函数式测试
    path('async/t0/', test0),  # 同步函数式测试
    path('async/t1/', test1),  # 特性测试
    path('async/t2/', test2),  # 特性测试
    path('async/t3/', test3),  # 特性测试
]

"""
curl "127.0.0.1:8000/async/t3" 会报 302
curl "127.0.0.1:8000/async/t3/"


"""