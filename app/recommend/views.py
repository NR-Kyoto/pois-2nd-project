from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
import json
from app.recommend.recommend import make_recommend_list

from app.recipe.models import Dish
from app.recipe.views import get_dish_info

# Create your views here.
# def recommend_recipe(request) -> HttpResponse:
#     body = json.loads(request.body)
#     recommend_recipe_list = make_recommend_list(body)
#     dishes = [Dish.objects.get(dish_id=d) for d in recommend_recipe_list]
#     d_list = [get_dish_info(d) for d in dishes]

#     return d_list

# class RecommendRecipeView(generics.GenericAPIView):
    
#     def get(self, request):
#         body = json.loads()
