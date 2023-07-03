from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect

class AuthMiddleware(MiddlewareMixin):
    def process_response(self, request, response):

        # 未ログイン
        if not request.user.is_authenticated:

            # ログインと登録はOK
            if ('/auth/' in request.path) or ('/auth/signup/' in request.path): 
                return response

            return HttpResponseRedirect('/auth/')


        return response