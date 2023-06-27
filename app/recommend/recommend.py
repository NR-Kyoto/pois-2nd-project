from models import RecipeGraph

# 入力：レシピのid
# 出力：レシピグラフでの入力の近傍{"id":同時に選ばれた回数}
def get_neighbour_ids(recipe_id):
    neighbor_recipes = RecipeGraph.objects.filter(id1_dish = recipe_id)
    neighbors = {}
    for recipe_edge in neighbor_recipes:
        neighbors[recipe_edge.id2_dish] = recipe_edge.num_selected
    return neighbors


# 入力の集合の共通の近傍を取る
# 重みは(今のところ)足し合わせていく
# 入力：現在のレシピのidリスト
# 出力：推薦レシピのidリスト
def make_recommend_list(recipe_ids, max_num=5):
    recommend_recipe_ids = {}
    for i, recipe in enumerate(recipe_ids):
        neighbour_ids = get_neighbour_ids(recipe)
        if not i:
            recommend_recipes = neighbour_ids
            continue
        for k in recommend_recipe_ids.keys():
            if k in neighbour_ids:
                recommend_recipe_ids[k] += neighbour_ids[k]
            else:
                # 全部の共通部分は条件が厳しすぎかも
                # 共通部分以外を消さずに追加しても良い?
                # recommend_recipe_ids[k] = neighbour_ids[k]
                recommend_recipe_ids.pop(k)     

    recommend_lists = sorted(recommend_recipe_ids.items(), key= lambda x: x[1])
    return recommend_lists[:max_num]
