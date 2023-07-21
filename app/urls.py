from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('', include('app.login.urls')),
    path('admin/', admin.site.urls),
    path('recipe/', include('app.recipe.urls')),
    path('recommend/', include('app.recommend.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)