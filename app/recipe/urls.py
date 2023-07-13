from django.urls import path
 
from .views import MergeRecipes, test

urlpatterns = [
    path('test', test, name='testpage'),
    path('', MergeRecipes.as_view(), name='merge'),
]