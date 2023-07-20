from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_406_NOT_ACCEPTABLE

from .scheduler import RecipeScheduler

from app.recipe.models import Menu, MenuDetail, Dish, CookingTool
from app.recommend.models import RecipeGraph

from rest_framework.views import APIView
from rest_framework import status

class MergeRecipes(APIView):
    
    def post(self, request, *args, **kwargs):
        
        # ユーザ認証
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        recipes = request.data['recipes'] # 献立のレシピ

        # 空配列
        if len(recipes) == 0:
            return Response({"error": "No recipes"}, status=HTTP_406_NOT_ACCEPTABLE)

        try:
            # scheduler = RecipeScheduler(user=request.user, dishes=request.data['recipes'], limit_time=20)
            scheduler = RecipeScheduler(user=request.user, dishes=request.data['recipes'])
            schedule = scheduler.scheduling()

            del scheduler 

            return Response(schedule)

        except ValueError as e:
            print(e)
            return Response({"error": "cannot make scheduler"}, status=HTTP_406_NOT_ACCEPTABLE)
        
# get all of the menu
        
class getRecipe(APIView):
    

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)
    
        dish_list = Dish.objects.all()
        return Response(
            {
                "dish_list": [
                    {
                        "dish_id": dish.dish_id,
                        "dish_name": dish.dish_name
                    }
                    for dish in dish_list
                ]
            },
            status=status.HTTP_200_OK
        )


from django.http import HttpResponse, HttpRequest
from app.recipe.models import Menu, MenuDetail, Dish, CookingTool
from app.recommend.models import RecipeGraph
import json

def cal_total_time(dish_id: int) -> int:
    '''
    一つの料理の合計時間
    '''
    try:
        obj = Dish.objects.get(dish_id=dish_id)
        time = 0
        for p in obj.manual["procedure"]:
            time += p["time"]
        return time
    except Dish.DoesNotExist as e:
        print(e)
        return -1

def get_recipe_procedure(dish_id: int) -> list[str]:
    '''
    '''
    try:
        obj = Dish.objects.get(dish_id=dish_id)
        out_list = []
        for p in obj.manual["procedure"]:
            out_list.append(p["text"])
        return out_list
    except Dish.DoesNotExist as e:
        print(e)
        return [""]

def get_dish_info(dish: Dish) -> dict:
    d = {}
    d["id"] = dish.dish_id
    d["dish_name"] = dish.dish_name
    d["time"] = cal_total_time(dish.dish_id)
    d["ingredient"] = dish.manual["ingredient"]
    d["img_name"] = ""
    return d

def get_dish_detail_info(dish_id) -> dict:
    try:
        dish = Dish.objects.get(dish_id=dish_id)
        d = get_dish_info(dish)
        d["procedure"] = get_recipe_procedure(dish_id)
        return d
    except:
        return {}

def update_recipe_graph_table(dish_list: list[Dish]):
    # RecipeGraphの更新
    if len(dish_list) < 2: return None
    
    dish_list.sort(key=lambda d: d.dish_id)
    for i, dish1 in enumerate(dish_list):
        if i == len(dish_list)-1:break
        for dish2 in dish_list[i+1:]:
            obj, is_created = RecipeGraph.objects.get_or_create(dish1=dish1, dish2=dish2)
            obj.num_selected +=1
            obj.save()

def register_menu(request, dish_list: list[Dish]) -> None:
    '''
    ユーザがデータベースに献立を追加する時に使う関数
    '''
    #userの取得
    user = request.user

    dish_list.sort(key=lambda d: d.dish_id)
    # Menuの登録
    menu = Menu.objects.create(user=user)
    
    # MenuDetailの登録
    MenuDetail.objects.bulk_create([MenuDetail(menu=menu,dish=dish) for dish in dish_list]) 

    # RecipeGraphの更新
    update_recipe_graph_table(dish_list)

def get_menu_history(request) -> list:
    '''
    username から過去の献立履歴を取得する
    返り値は以下の通り
    [
        {"date" : date, "dish" : [dish1, dish2, ...]},
        {"date" : date, "dish" : [dish1, dish2, ...]},
        ...
    ]
    '''
    user = request.user
    menu_sets = Menu.objects.filter(user=user)

    history_list = []

    for menu in menu_sets:
        
        dishes = MenuDetail.objects.filter(menu=menu).values_list("dish")
        menu_dict = {"date":menu.date, "dish_names":[d.name for d in dishes]}
        history_list.append(menu_dict)
        
    return history_list

def make_or_update_cookingtool_info(request, tool_info:dict=None) -> None:
    '''
    ユーザの調理器具の情報を更新する関数
    tool_info = {
        "kitchen_knife": int #包丁
        "cutting_board": int #まな板
        "flying_pan": 
        "sauce_pan": 
        "bowl": 
        "stove" : int #コンロ
    }
    '''
    if tool_info is None:
        tool_info = {"kitchen_knife":0, "cutting_board":0, "flying_pan":0, "sauce_pan":0, "bowl":0, "stove":0}
    obj, is_created = CookingTool.objects.get_or_create(user=request.user)
    obj.kitchen_knife = tool_info["kitchen_knife"]
    obj.cutting_board = tool_info["cutting_board"]
    obj.flying_pan = tool_info["flying_pan"]
    obj.sauce_pan = tool_info["sauce_pan"]
    obj.bowl = tool_info["bowl"]
    obj.stove = tool_info["stove"]
def regist_menu(request: HttpRequest) -> HttpResponse:

    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            dish_obj_list = [Dish.objects.get(dish_id=id) for id in body]
            register_menu(request, dish_obj_list)
            return HttpResponse(json.dumps({"result": "Success"}, ensure_ascii=False))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({"result": "Failed"}, ensure_ascii=False))

    return HttpResponse('POST ONLY')

def search_dish(request: HttpRequest) -> HttpResponse:
    '''
    入力された文字列から部分マッチする料理を検索する
    '''
    body = json.loads(request.body)
    dishes = Dish.objects.filter(name__contains=body["search_str"]).values_list("dish_name")
    out = [get_dish_info(dish) for dish in dishes]
    out = json.dumps(out, ensure_ascii=False)

    return HttpResponse(out)

def show_dish_info(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        print(request.body)
        body = json.loads(request.body)
        d = get_dish_detail_info(body["id"])
        return HttpResponse(json.dumps(d, ensure_ascii=False))
    
    return HttpResponse('POST ONLY')

def regist_cookingtool_info(request: HttpRequest) -> HttpResponse:
    body = json.loads(request.body)
    make_or_update_cookingtool_info(request, body)

def show_menu_history(request) -> HttpResponse:
    l = get_menu_history(request)
    return HttpResponse(json.dumps(l, ensure_ascii=False))
