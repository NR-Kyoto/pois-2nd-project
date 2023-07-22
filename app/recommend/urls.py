from django.urls import path
from .views import RecommendRecipe

urlpatterns = [
    path('recommend_recipe/', RecommendRecipe.as_view(), name='recommend_recipe'),
]