from django.shortcuts import render
from django.http import HttpResponse
import json
from app.recommend.recommend import make_recommend_list

from app.recipe.models import Dish
from app.recipe.views import get_dish_info

# Create your views here.
def recommend_recipe(request) -> HttpResponse:
    body = json.loads(request.body)
    recommend_recipe_list = make_recommend_list(body)
    dishes = [Dish.objects.get(dish_id=d) for d in recommend_recipe_list]
    d_list = [get_dish_info(d) for d in dishes]
    return HttpResponse(json.dumps(d_list, ensure_ascii=False))
