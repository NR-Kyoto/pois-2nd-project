from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model

from recipe.models import Menu, MenuDetail, Dish, CookingTool
from recommend.models import RecipeGraph
from recipe.views import *
import datetime

UserModel = get_user_model()

class RecipeTestCase(TestCase):

    # fixtures = ["db_dish.json"] # <- jsonファイルで書いたデータをDBに読み込む

    def setUp(self):

        self.user = UserModel.objects.create(
            username="kanade"
        )
        self.dish1 = Dish.objects.create(
            dish_name="karubi",
            manual={}
        )
        self.dish2 = Dish.objects.create(
            dish_name="tamagoyaki",
            manual={}
        )
        self.dish3 = Dish.objects.create(
            dish_name="ice cream",
            manual={}
        )
        self.request = RequestFactory()
        self.request.user = self.user
    
    def test_case1(self):
        
        self.client.force_login(self.user) # ログイン
        make_or_update_cookingtool_info(self.request)
        cookinfo_obj = CookingTool.objects.get(user=self.user)
        self.assertEqual(cookinfo_obj.user, self.user)
        self.assertEqual(cookinfo_obj.kitchen_knife, 0)

    def test_addmenu_and_gethistroy(self):
        self.client.force_login(self.user)
        register_menu(self.request, [self.dish2, self.dish1])
        register_menu(self.request, [self.dish1, self.dish2, self.dish3])
        self.assertEqual(get_menu_history(self.request), [{'date': datetime.date.today(), 'dish': [(1,), (2,)]}, {'date': datetime.date.today(), 'dish': [(1,), (2,), (3,)]}])
        objs = RecipeGraph.objects.filter(dish1=self.dish1)
        obj=objs[0]
        self.assertEqual((obj.dish1, obj.dish2, obj.num_selected), (self.dish1, self.dish2, 2))
        obj=objs[1]
        self.assertEqual((obj.dish1, obj.dish2, obj.num_selected), (self.dish1, self.dish3, 1))
        








