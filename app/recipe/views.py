from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK
from rest_framework.views import APIView
from app.recipe.scheduler import RecipeScheduler

from app.recipe.models import Menu, MenuDetail, Dish, CookingTool
from app.recommend.models import RecipeGraph

import json


class MergeRecipes(APIView):

    def post(self, request, *args, **kwargs):

        # ユーザ認証
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        recipes = request.data['recipes']  # 献立のレシピ

        # 空配列
        if len(recipes) == 0:
            return Response({"error": "No recipes"}, status=HTTP_406_NOT_ACCEPTABLE)

        try:
            scheduler = RecipeScheduler(user=request.user, dishes=request.data['recipes'], limit_time=20)
            # scheduler = RecipeScheduler(user=request.user, dishes=request.data['recipes'])
            schedule = scheduler.scheduling()

            del scheduler

            
            register_menu(request, dish_list=[Dish.objects.get(dish_id=dish_id) for dish_id in recipes])

            return Response(schedule)

        except ValueError as e:
            print(e)
            return Response({"error": "cannot make scheduler"}, status=HTTP_406_NOT_ACCEPTABLE)


# get all the menu

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
                        "dish_name": dish.dish_name,
                        "ingredient": ', '.join(dish.manual["ingredient"].keys()),
                        "dish_image": dish.image,
                        "dish_manual": dish.manual,
                        "time": round(cal_total_time(dish.dish_id) / 60)
                    }
                    for dish in dish_list
                ]
            },
            status=HTTP_200_OK
        )

def cal_total_time(dish_id: int) -> int:
    '''
    一つの料理の合計時間
    '''
    try:
        obj = Dish.objects.get(dish_id=dish_id)
        time = 0
        for p in obj.manual["procedure"]:
            time += int(p["time"])
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


def get_host_url(request: HttpRequest) -> str:
    return "http://" + request.META.get("HTTP_HOST")


def get_dish_image_url(dish: Dish, hosturl: str) -> str:
    url = dish.get_image_url()
    return hosturl + "/" + url


def get_dish_info(dish: Dish, hosturl) -> dict:
    d = {}
    d["id"] = dish.dish_id
    d["dish_name"] = dish.dish_name
    d["time"] = cal_total_time(dish.dish_id)
    d["ingredient"] = dish.manual["ingredient"]
    d["img_url"] = get_dish_image_url(dish, hosturl)
    # d["img_url"] = dish.dish_image
    return d


def get_dish_detail_info(dish_id, hosturl) -> dict:
    try:
        dish = Dish.objects.get(dish_id=dish_id)
        d = get_dish_info(dish, hosturl)
        d["procedure"] = get_recipe_procedure(dish_id)
        return d
    except:
        return {}


def update_recipe_graph_table(dish_list: list[Dish]):
    # RecipeGraphの更新
    if len(dish_list) < 2: return None

    dish_list.sort(key=lambda d: d.dish_id)
    for i, dish1 in enumerate(dish_list):
        if i == len(dish_list) - 1: break
        for dish2 in dish_list[i + 1:]:
            obj, is_created = RecipeGraph.objects.get_or_create(dish1=dish1, dish2=dish2)
            obj.num_selected += 1
            obj.save()


def register_menu(request, dish_list: list[Dish]) -> None:
    '''
    ユーザがデータベースに献立を追加する時に使う関数
    '''
    # userの取得
    user = request.user

    dish_list.sort(key=lambda d: d.dish_id)
    # Menuの登録
    menu = Menu.objects.create(user=user)

    # MenuDetailの登録
    MenuDetail.objects.bulk_create([MenuDetail(menu=menu, dish=dish) for dish in dish_list])

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
        dishes = MenuDetail.objects.filter(menu=menu).values("dish")
        menu_dict = {"date": str(menu.date), "dish_names": [Dish.objects.get(dish_id=d['dish']).dish_name for d in dishes]}
        history_list.append(menu_dict)

    return history_list


def get_cookingtool_info(user) -> dict:
    obj, is_created = CookingTool.objects.get_or_create(user=user)
    tool_info = {"kitchen_knife": obj.kitchen_knife, "cutting_board": obj.cutting_board, "flying_pan": obj.flying_pan,
                 "sauce_pan": obj.sauce_pan, "bowl": obj.bowl, "stove": obj.stove}
    return tool_info


def make_or_update_cookingtool_info(request, tool_info_input: dict = None) -> None:
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
    obj, is_created = CookingTool.objects.get_or_create(user=request.user)  # デフォルトは全部 1
    tool_info = get_cookingtool_info(request.user)
    if type(tool_info) is dict:
        tool_info.update(tool_info_input)

    obj.kitchen_knife = tool_info["kitchen_knife"]
    obj.cutting_board = tool_info["cutting_board"]
    obj.flying_pan = tool_info["flying_pan"]
    obj.sauce_pan = tool_info["sauce_pan"]
    obj.bowl = tool_info["bowl"]
    obj.stove = tool_info["stove"]
    obj.save()
    return HttpResponse(json.dumps({"result": "Success"}, ensure_ascii=False))


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
    '''f
    入力された文字列から部分マッチする料理を検索する
    '''
    if request.method == 'POST':

        try:
            body = json.loads(request.body)
            hosturl = get_host_url(request)
            dishes = Dish.objects.filter(name__contains=body["search_str"]).values_list("dish_name")
            out = [get_dish_info(dish, hosturl) for dish in dishes]
            out = json.dumps(out, ensure_ascii=False)
            return HttpResponse(out)
        except Exception as e:
            print(e)
            return HttpResponse({'error': 'cannot get dishes'})

    return HttpResponse('POST ONLY')


def show_dish_info(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        print(request.body)
        body = json.loads(request.body)
        d = get_dish_detail_info(body["id"], get_host_url(request))
        return HttpResponse(json.dumps(d, ensure_ascii=False))

    return HttpResponse('POST ONLY')


def regist_cookingtool_info(request: HttpRequest) -> HttpResponse:
    '''
    ユーザの調理器具に関する情報を登録する
    全部まとめての登録だけではなく、一つ一つ指定して登録することも可能
    (例) request.body = {"bowl":0}
    '''
    body = json.loads(request.body)
    make_or_update_cookingtool_info(request, body)
    return HttpResponse(json.dumps({"result": "Success"}, ensure_ascii=False))


def show_cookingtool_info(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        tool_info = get_cookingtool_info(request.user)
        return HttpResponse(json.dumps(tool_info, ensure_ascii=False))
    return HttpResponse('POST ONLY')


def show_menu_history(request) -> HttpResponse:
    l = get_menu_history(request)
    return HttpResponse(json.dumps(l, ensure_ascii=False))


def get_dish_image_url_response(request: HttpRequest) -> HttpResponse:
    '''
    入力データ e.x.{"id" : 2} を受け取り、料理の写真のURLを返す
    '''
    if request.method == "POST":
        body = json.loads(request.body)
        try:
            dish = Dish.objects.get(dish_id=body["id"])
            url = get_dish_image_url(dish, get_host_url(request))
            return HttpResponse({'url': url})
        except Exception as e:
            print(e)
            return HttpResponse({'error': 'cannot get dish_image url'})
    return HttpResponse('POST ONLY')


class RegistMenu(APIView):

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request)
            dish_obj_list = [Dish.objects.get(dish_id=id) for id in body]
            register_menu(request, dish_obj_list)
            return Response(json.dumps({"result": "Success"}, ensure_ascii=False))
        except Exception as e:
            print(e)
            return Response(json.dumps({"result": "Failed"}, ensure_ascii=False))


class SearchDish(APIView):

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            hosturl = get_host_url(request)
            dishes = Dish.objects.filter(dish_name__contains=body["search_str"])
            out = [get_dish_info(dish, hosturl) for dish in dishes]
            out = json.dumps(out, ensure_ascii=False)
            return Response(out)
        except Exception as e:
            print(e)
            return Response({'error': 'cannot get dishes'})


class ShowDishInfo(APIView):

    def get(self, request, *args, **kwargs):
        body = json.loads(request.body)
        d = get_dish_detail_info(body["id"], get_host_url(request))
        return Response(json.dumps(d, ensure_ascii=False))


class ShowCookingToolInfo(APIView):

    def get(self, request, *args, **kwargs):
        tool_info = get_cookingtool_info(request.user)
        return Response(json.dumps(tool_info, ensure_ascii=False))


class RegistCookingToolInfo(APIView):

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        make_or_update_cookingtool_info(request, body)
        return Response(json.dumps({"result": "Success"}, ensure_ascii=False))


class ShowMenuHistory(APIView):

    def get(self, request, *args, **kwargs):
        l = get_menu_history(request)
        return Response(json.dumps(l, ensure_ascii=False))


class GetDishImageURL(APIView):

    def get(self, request, *args, **kwargs):
        body = json.loads(request.body)
        try:
            dish = Dish.objects.get(dish_id=body["id"])
            url = get_dish_image_url(dish, get_host_url(request))
            return Response({'url': url})
        except Exception as e:
            print(e)
            return Response({'error': 'cannot get dish_image url'})
