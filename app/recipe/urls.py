from django.urls import path
from .views import MergeRecipes, RegistMenu, SearchDish, ShowDishInfo, ShowCookingToolInfo, RegistCookingToolInfo, ShowMenuHistory, GetDishImageURL, getRecipe

urlpatterns = [
    path('regist_menu/', RegistMenu.as_view(), name='regist_menu'),
    path('search_dish/', SearchDish.as_view(), name='search_dish'),
    path('show_dish_info/', ShowDishInfo.as_view(), name='show_dish_info'),
    path('show_cookingtool_info', ShowCookingToolInfo.as_view(), name='show_cookingtool_info'),
    path('regist_cookingtool_info/', RegistCookingToolInfo.as_view(), name='regist_cookingtool_info'),
    path('show_menu_history/', ShowMenuHistory.as_view(), name='show_menu_history'),
    path('get_image_url/', GetDishImageURL.as_view(), name='get_dish_image_url'),
    path('mergeRecipe/', MergeRecipes.as_view(), name='merge'),
    path('getRecipe/', getRecipe.as_view(), name='get Recipe'),
]
