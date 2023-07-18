from django.test import TestCase
from recipe.models import Dish
from recommend.models import RecipeGraph
from recommend.recommend import make_recommend_list

# Create your tests here.

class RecommendTests(TestCase):
    # def setup(self):
    #     print("setup")
    #     self.dish1 = Dish.objects.create(dish_id = 1, dish_name = "a", manual = {})
    #     self.dish2 = Dish.objects.create(dish_id = 2, dish_name = "b", manual = {})
    #     self.dish3 = Dish.objects.create(dish_id = 3, dish_name = "c", manual = {})
    #     self.dish4 = Dish.objects.create(dish_id = 4, dish_name = "d", manual = {})
    #     self.dish5 = Dish.objects.create(dish_id = 5, dish_name = "e", manual = {})
    #     RecipeGraph.objects.create(dish1=self.dish2, dish2=self.dish3, num_selected=5)
    #     RecipeGraph.objects.create(dish1=self.dish2, dish2=self.dish4, num_selected=4)
    #     RecipeGraph.objects.create(dish1=self.dish1, dish2=self.dish2, num_selected=3)
    #     RecipeGraph.objects.create(dish1=self.dish1, dish2=self.dish5, num_selected=3)
    #     RecipeGraph.objects.create(dish1=self.dish1, dish2=self.dish2, num_selected=3)

    def test_one_recipe(self):
        self.dish1 = Dish.objects.create(dish_id = 1, dish_name = "a", manual = {})
        self.dish2 = Dish.objects.create(dish_id = 2, dish_name = "b", manual = {})
        self.dish3 = Dish.objects.create(dish_id = 3, dish_name = "c", manual = {})
        self.dish4 = Dish.objects.create(dish_id = 4, dish_name = "d", manual = {})
        self.dish5 = Dish.objects.create(dish_id = 5, dish_name = "e", manual = {})
        RecipeGraph.objects.create(dish1=self.dish2, dish2=self.dish3, num_selected=5)
        RecipeGraph.objects.create(dish1=self.dish2, dish2=self.dish4, num_selected=4)
        RecipeGraph.objects.create(dish1=self.dish1, dish2=self.dish2, num_selected=3)
        RecipeGraph.objects.create(dish1=self.dish1, dish2=self.dish5, num_selected=3)
        RecipeGraph.objects.create(dish1=self.dish1, dish2=self.dish3, num_selected=3)
        """
        一つのレシピが与えられたとき
        """
        recommend_list = make_recommend_list([2])
        self.assertEqual(recommend_list, [(3,5),(4,4),(1,3)])
        recommend_list = make_recommend_list([1,2])
        self.assertEqual(recommend_list, [(3,8)])
        recommend_list = make_recommend_list([1,2,3])
        self.assertEqual(recommend_list, [])
        recommend_list = make_recommend_list([10])
        self.assertEqual(recommend_list, [])