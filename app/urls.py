'''
Author: dnimo kuochingcha@gmail.com
Date: 2023-07-04 17:32:30
LastEditors: dnimo kuochingcha@gmail.com
LastEditTime: 2023-07-04 23:00:49
FilePath: /pois-2nd-project/app/urls.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.login.urls')),
    path('recipe/', include('app.recipe.urls')),
    path('recommend/', include('app.recommend.urls')),
]