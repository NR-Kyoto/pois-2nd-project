from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', include('app.login.urls')),
    path('admin/', admin.site.urls),
    path('recipe/', include('app.recipe.urls')),
    path('recommend/', include('app.recommend.urls')),
    path('merge/', include('app.recipe.urls'))
]