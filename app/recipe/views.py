from django.shortcuts import render
from recipe.models import Menu, MenuDetail, Dish, CookingTool
from recommend.models import RecipeGraph

def update_recipe_graph_table(dish_id_list: list):
    # RecipeGraphの更新
    if len(dish_id_list) < 2: return None
    
    dish_id_list.sort()
    for i, id1 in enumerate(dish_id_list):
        if i == len(dish_id_list-1):break
        for id2 in dish_id_list[i+1:]:
            obj, is_created = RecipeGraph.objects.get_or_create(id1_dish=id1, id2_disg=id2)
            obj.num_selected +=1
            obj.save()

def register_menu(request, dish_id_list: list) -> None:
    '''
    ユーザがデータベースに献立を追加する時に使う関数
    '''
    #usernameの取得
    username = request.user.get_username()

    dish_id_list = dish_id_list.sort()
    # Menuの登録
    menu = Menu.objects.create(username=username)
    
    # MenuDetailの登録
    MenuDetail.objects.bulk_create([MenuDetail(menu_id=menu.menu_id,dish_id=i) for i in dish_id_list]) 

    # RecipeGraphの更新
    update_recipe_graph_table(dish_id_list)

def get_menu_history(request) -> list:
    '''
    username から過去の献立履歴を取得する
    返り値は以下の通り
    [
        {"date" : date, "dish_name" : [dish1, dish2, ...]},
        {"date" : date, "dish_name" : [dish1, dish2, ...]},
        ...
    ]
    '''
    username = request.user.get_username()
    menu_sets = Menu.objects.filter(username=username)

    history_list = []

    for menu in menu_sets:
        
        dish_ids = MenuDetail.objects.filter(menu_id=menu.menu_id).values_list("dish_id")
        dish_names = Dish.objects.filter(dish_id__in=dish_ids).values_list("dish_name")
        menu_dict = {"date":menu_sets.date, "dish_name":list(dish_names)}
        history_list.append(menu_dict)
        
    return history_list
    
def search_dish(input:str) -> list:
    '''
    入力された文字列から部分マッチする料理を検索する
    '''
    dishes = Dish.objects.filter(name__contains=input).values_list("dish_name")
    return list(dishes)

def update_cookingtool_info(request, tool_info:dict) -> None:
    '''
    ユーザの調理器具の情報を更新する関数
    tool_info = {
        "kitchen_knife": int #包丁
        "cutting_board": int #まな板
        "stove" : int #コンロ
    }
    '''
    username = request.user.get_username()
    obj, is_created = CookingTool.objects.get_or_create(username=username)
    obj.kitchen_knife = tool_info["kitchen_knife"]
    obj.cutting_board = tool_info["cutting_board"]
    obj.stove = tool_info["stove"]

