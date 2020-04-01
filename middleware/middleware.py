# 这里和上面截图里的代码不同，以这里为准

from App.models import AXFUser
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

# 返回 json
R_LOGIN_JSON = [
    '/axf/addtocart/',
    '/axf/subtocart/',

]

# 返回 重定向
R_LOGIN = [
    '/axf/cart/',

]


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):

        if request.path in R_LOGIN_JSON:
            user_id = request.session.get('user_id')
            # 已登录
            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    request.user = user

                except:
                    data = {
                        "status": 301,
                        "msg": "用户状态失效"
                    }
                    return JsonResponse(data=data)
            # 未登录
            else:
                data = {
                    "status": 301,
                    "msg": "用户状态失效"
                }
                return JsonResponse(data=data)
        if request.path in R_LOGIN:
            user_id = request.session.get('user_id')
            # 已登录
            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    request.user = user

                except:
                    return redirect(reverse("axf:login"))
            # 未登录
            else:
                return redirect(reverse("axf:login"))
