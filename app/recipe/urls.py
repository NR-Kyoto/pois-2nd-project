from django.urls import path
 
from .views import MergeRecipes

urlpatterns = [
    path('', MergeRecipes.as_view(), name='merge'),
]