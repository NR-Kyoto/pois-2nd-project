from app.recipe.models import Dish
from app.recommend.models import RecipeGraph

from django.db.models import Q

from collections import defaultdict

# 入力：レシピのid
# 出力：レシピグラフでの入力の近傍{"id":同時に選ばれた回数}
def get_neighbour_ids(recipe_id):
    try:
        input = Dish.objects.get(dish_id = recipe_id)
    except Dish.DoesNotExist as e:
        print(e)
        return {}

    neighbor_recipes = RecipeGraph.objects.filter(Q(dish1 = input) | Q(dish2 = input))
    neighbors = {}
    for recipe_edge in neighbor_recipes:
        if recipe_edge.dish1.dish_id == recipe_id:
            neighbors[recipe_edge.dish2.dish_id] = recipe_edge.num_selected
        elif recipe_edge.dish2.dish_id == recipe_id:
            neighbors[recipe_edge.dish1.dish_id] = recipe_edge.num_selected
        #print(neighbors)

    return neighbors


# 入力の集合の共通の近傍を取る
# 重みは(今のところ)足し合わせていく
# 入力：現在のレシピのidリスト
# 出力：推薦レシピのidリスト
def make_recommend_list(recipe_ids, max_num=5):
    recommend_recipe_ids = defaultdict(int)
    for i, recipe_id in enumerate(recipe_ids):
        neighbour_ids = get_neighbour_ids(recipe_id)
        # if not i:
        #     recommend_recipe_ids = neighbour_ids
        #     continue
        # ids = list(recommend_recipe_ids.keys())
        # for k in ids:
        #     if k in neighbour_ids:
        #         recommend_recipe_ids[k] += neighbour_ids[k]
        #     else:
        #         # 全部の共通部分は条件が厳しすぎかも
        #         # 共通部分以外を消さずに追加しても良い?
        #         # recommend_recipe_ids[k] = neighbour_ids[k]
        #         recommend_recipe_ids.pop(k)  
        for k in list(neighbour_ids.keys()): 
            recommend_recipe_ids[k] += neighbour_ids[k]

    recommend_lists = sorted(recommend_recipe_ids.items(), key= lambda x: x[1], reverse=True)
    return recommend_lists[:max_num]
