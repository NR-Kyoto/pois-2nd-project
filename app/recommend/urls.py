from django.urls import path
from .views import RecommendRecipeView

urlpatterns = [
    path('recommend_recipe/', RecommendRecipeView.as_view(), name='recommend_recipe'),
]