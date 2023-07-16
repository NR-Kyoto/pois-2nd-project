from django.urls import path
from .views import regist_menu, search_dish, show_dish_info, regist_cookingtool_info, show_menu_history, get_dish_image_url_response
from .views import MergeRecipes

urlpatterns = [
    path('regist_menu/', regist_menu, name='regist_menu'),
    path('search_dish/', search_dish, name='search_dish'),
    path('show_dish_info/', show_dish_info, name='show_dish_info'),
    path('regist_cookingtool_info/', regist_cookingtool_info, name='regist_cookingtool_info'),
    path('show_menu_history/', show_menu_history, name='show_menu_history'),
    path('get_image_url/', get_dish_image_url_response, name='get_dish_image_url'),
    path('merge/', MergeRecipes.as_view(), name='merge'),
]
