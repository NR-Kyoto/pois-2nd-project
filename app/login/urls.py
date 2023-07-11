'''
Author: dnimo kuochingcha@gmail.com
Date: 2023-07-03 16:01:32
LastEditors: dnimo kuochingcha@gmail.com
LastEditTime: 2023-07-04 17:48:57
FilePath: /pois-2nd-project/app/login/urls.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from django.urls import path
from .views import CreateUserView, ObtainTokenView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', ObtainTokenView.as_view(), name='login'),
]