from django.shortcuts import render
from recipe.models import Menu, MenuDetail, Dish, CookingTool
from recommend.models import RecipeGraph

def update_recipe_graph_table(dish_list: list):
    # RecipeGraphの更新
    if len(dish_list) < 2: return None
    
    dish_list.sort(key=lambda d: d.dish_id)
    for i, dish1 in enumerate(dish_list):
        if i == len(dish_list)-1:break
        for dish2 in dish_list[i+1:]:
            obj, is_created = RecipeGraph.objects.get_or_create(dish1=dish1, dish2=dish2)
            obj.num_selected +=1
            obj.save()

def register_menu(request, dish_list: list) -> None:
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
        menu_dict = {"date":menu.date, "dish":list(dishes)}
        history_list.append(menu_dict)
        
    return history_list
    
def search_dish(input:str) -> list:
    '''
    入力された文字列から部分マッチする料理を検索する
    '''
    dishes = Dish.objects.filter(name__contains=input).values_list("dish_name")
    return list(dishes)

def make_or_update_cookingtool_info(request, tool_info:dict=None) -> None:
    '''
    ユーザの調理器具の情報を更新する関数
    tool_info = {
        "kitchen_knife": int #包丁
        "cutting_board": int #まな板
        "stove" : int #コンロ
    }
    '''
    if tool_info is None:
        tool_info = {"kitchen_knife":0, "cutting_board":0, "stove":0}
    obj, is_created = CookingTool.objects.get_or_create(user=request.user)
    obj.kitchen_knife = tool_info["kitchen_knife"]
    obj.cutting_board = tool_info["cutting_board"]
    obj.stove = tool_info["stove"]

