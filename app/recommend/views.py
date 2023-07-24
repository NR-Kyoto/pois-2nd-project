from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from django.http import HttpResponse, HttpRequest
import json
from app.recommend.recommend import make_recommend_list

from app.recipe.models import Dish
from app.recipe.views import get_dish_info, get_host_url, cal_total_time
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK
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

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        recommend_recipe_list = make_recommend_list(body)
        host_url = get_host_url(request)
        print(recommend_recipe_list)
        dishes = [Dish.objects.get(dish_id=d[0]) for d in recommend_recipe_list]
        # d_list = [get_dish_info(d, host_url) for d in dishes]
        return Response(
            {
                "dish_list": [
                    {
                        "dish_id": dish.dish_id,
                        "dish_name": dish.dish_name,
                        "ingredient": ', '.join(dish.manual["ingredient"].keys()),
                        "dish_image": dish.image,
                        "dish_manual": dish.manual,
                        "time": round(cal_total_time(dish.dish_id) / 60)
                    }
                    for dish in dishes
                ]
            },
            status=HTTP_200_OK
        )

