from django.urls import path
from .views import CreateUserView, ObtainTokenView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', ObtainTokenView.as_view(), name='login'),
]