# レシピの推薦

# アルゴリズム
# 入力の集合の共通の近傍を取る
# 重みは(今のところ)足し合わせていく
    
# 入力：レシピのid
# 出力：レシピグラフでの入力の近傍{"id":同時に選ばれた回数}
def get_neighbours(recipe):
    # TODO データベースからrecipeの近傍(料理, 重み)をとる
    # results(list) = Member.objects.all().filter(first_name="office")
    neighbors = {"name":1} # 辞書で返す
    return neighbors

# 入力：現在のレシピのidリスト
# 出力：推薦レシピのidリスト
def make_recommend_list(recipes, max_num=5):
    recommend_recipes = {}
    for i, recipe in enumerate(recipes):
        neighbours = get_neighbours(recipe)
        if not i:
            recommend_recipes = neighbours
            continue
        for k in recommend_recipes.keys():
            if k in neighbours:
                recommend_recipes[k] += neighbours[k]
            else:
                # 全部の共通部分は条件が厳しすぎかも
                # 共通部分以外を消さずに追加しても良い?
                # recommend_recipes[k] = neighbours[k]
                recommend_recipes.pop(k)     

    recommend_lists = sorted(recommend_recipes.items(), key= lambda x: x[1])
    return recommend_lists[:max_num]
