import time
import traceback
import logging
import ujson as json
from django.http import HttpResponse, HttpRequest
from django.core.signing import TimestampSigner
from django.core.signing import SignatureExpired
from django.views import View
from base import errors
from base.check_params import CheckParams
from pprint import pprint

error_logger = logging.getLogger('error')
access_logger = logging.getLogger('gunicorn')


class BaseApi(View):
    """Rest Api"""
    NEED_LOGIN = True
    NEED_PERMISSION = True
    need_params = {}

    def _get_token(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise errors.LoginExpireError
        return token

    def _token2user_id(self, token):
        signer = TimestampSigner()
        try:
            # 如果加上max_age就可以控制登录有效时长
            max_age = 12 * 60 * 60
            user_id = signer.unsign(token, max_age=max_age)
        except SignatureExpired as e:
            raise errors.LoginExpireError
        return int(user_id)

    def _identification(self, request):
        token = self._get_token(request)
        user_id = self._token2user_id(token)
        request.user = self._check_user(user_id)
        request.user_id = user_id

    def _check_user(self, user_id):
        from account.models import UserModel
        user = UserModel.objects.filter(id=user_id, status=UserModel.ST_NORMAL).first()
        if not user:
            raise errors.LoginExpireError
        return user

    def _permission(self, user_id, url):
        '''
        权限验证
        '''
        from account.controllers.user import has_permission
        if not has_permission(user_id, url):
            raise errors.CommonError('权限不足，无法进行此操作')

    def _pre_handle(self, request: HttpRequest):
        '''
        请求预处理
        '''
        if self.NEED_LOGIN:
            self._identification(request)
            if self.NEED_PERMISSION:
                self._permission(request.user_id, request.path)
        request._start_time = time.time()  # 可以设置request,改变或新增请求上下文

    def _next_handle(self, request: HttpRequest, result: dict):
        """下一步"""
        time.sleep(1)

    def _end_handle(self, request: HttpRequest, result: dict):  # 设置下类型注释,方便idea代码提示
        """请求后处理"""
        if hasattr(request, '_start_time'):
            pprint("processing request spends time {} seconds".format(time.time() - request._start_time))
        return HttpResponse(json.dumps(result), content_type='application/json')

    def dispatch(self, request, *args, **kwargs):
        code = 0
        msg = ''
        data = {}

        try:
            self._pre_handle(request)
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            params = self.check_params(request)
            # 需要登录的接口，参数中自动增加operator参数
            if self.NEED_LOGIN:
                params['operator'] = request.user
            data = handler(request, params, *args, **kwargs)
        except errors.BaseError as e:
            traceback.print_exc()
            code = e.errcode
            msg = e.errmsg
        except Exception as e:
            # TODO: 记录log
            traceback.print_exc()
            error_logger.exception(e)
            code = errors.BaseError.errcode
            msg = errors.BaseError.errmsg
        result = {
            'code': code,
            'msg': msg,
            'data': data,
        }
        # pprint(result)
        if request.method.lower() != 'get':
            log_data = {
                'url': request.get_full_path(),
                'params': request.body,
                'user_id': getattr(request, 'user_id', None),
                'result': result,
            }
            access_logger.info(log_data)
        pprint(result)
        self._next_handle(request, result)
        return self._end_handle(request, result)

    def check_params(self, request):
        '''
        校验参数
        '''
        params = {}
        data = {}
        # 先解析url中的参数
        for k, v in request.GET.items():
            data[k] = v
        # 再解析body中的参数，存在相同参数时，以body中为准
        if request.body:
            data.update(json.loads(request.body))
        for key in self.need_params.keys():
            value = data.get(key)
            name, condition = self.need_params.get(key)
            method, *condition = condition.split(' ')
            method = 'check_{}'.format(method)
            value = getattr(CheckParams, method)(name, value, condition)
            params[key] = value
        return params
