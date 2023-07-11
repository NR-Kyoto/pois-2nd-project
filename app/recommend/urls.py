from django.urls import path
from .views import recommend_recipe

urlpatterns = [
    path('recommend_recipe/', recommend_recipe, name='recommend_recipe'),
]