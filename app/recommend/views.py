from django.shortcuts import render
from django.http import HttpResponse
import json
from app.recommend.recommend import make_recommend_list

from app.recipe.models import Dish
from app.recipe.views import get_dish_info, get_host_url
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView

# Create your views here.
def recommend_recipe(request) -> HttpResponse:
    body = json.loads(request.body)
    recommend_recipe_list = make_recommend_list(body)
    host_url = get_host_url(request)
    dishes = [Dish.objects.get(dish_id=d) for d in recommend_recipe_list]
    d_list = [get_dish_info(d, host_url) for d in dishes]
    return HttpResponse(json.dumps(d_list, ensure_ascii=False))

class RecommendRecipe(APIView):
    
    def get(self, request, *args, **kwargs):
        body = json.loads(request.body)
        recommend_recipe_list = make_recommend_list(body)
        host_url = get_host_url(request)
        dishes = [Dish.objects.get(dish_id=d) for d in recommend_recipe_list]
        d_list = [get_dish_info(d, host_url) for d in dishes]
        return Response(json.dumps(d_list, ensure_ascii=False))

