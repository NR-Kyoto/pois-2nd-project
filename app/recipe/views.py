from django.shortcuts import render
from recipe.models import Menu, MenuDetail
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

# 献立をデータベースに追加する
def register_menu(request, dish_id_list: list):
    #usernameの取得
    username = request.user.get_username()

    dish_id_list = dish_id_list.sort()
    # Menuの登録
    menu = Menu.objects.create(username=username)
    
    # MenuDetailの登録
    MenuDetail.objects.bulk_create([MenuDetail(menu_id=menu.menu_id,dish_id=i) for i in dish_id_list]) 

    # RecipeGraphの更新
    update_recipe_graph_table(dish_id_list)

# username から過去の献立履歴を取得する
def get_menu_history(request):
    username = request.user.get_username()
    


# 料理を検索(文字列)




