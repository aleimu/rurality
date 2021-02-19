__doc__ = "想做一个公共组件"
import json
from django.views import View
from django.views.generic import ListView
from rest_framework.views import APIView
from django.http.response import JsonResponse


class BaseView(APIView):
    def Json(self, code=1000, msg=None, data=None):
        return JsonResponse({'code': code, 'msg': msg, 'data': data})


def Json(code=1000, msg=None, data=None):
    return JsonResponse({'code': code, 'msg': msg, 'data': data})
