from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
## https://zenn.dev/shimakaze_soft/scraps/22dcea1acd133a

# データは一括作成、一括更新の方が良い

class Dish(models.Model):
    dish_id = models.AutoField(primary_key=True)
    dish_name = models.CharField(max_length = 50)
    manual = models.JSONField()

class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(
            get_user_model(),
            on_delete=models.DO_NOTHING, # userの削除時、何もしない
        )
    date = models.DateField(auto_now=True) # デフォルトは現在の時刻を設定
    
class MenuDetail(models.Model):
    menu_id = models.ForeignKey(
            Menu,
            on_delete=models.CASCADE,
        )
    dish_id = models.ForeignKey(
            Dish,
            on_delete=models.CASCADE,
        )

# 調理器具名は https://english.sps10.com/4956/ を参照
class CookingTool(models.Model):
    username = models.ForeignKey(
            get_user_model(),
            on_delete=models.CASCADE,
        )
    #包丁
    kitchen_knife = models.IntegerField(
            default=0,
            validators=[MinValueValidator(0), MaxValueValidator(100)]
        )
    #まな板
    cutting_board = models.IntegerField(
            default=0,
            validators=[MinValueValidator(0), MaxValueValidator(100)]
        )
    #コンロ
    stove = models.IntegerField(
            default=0,
            validators=[MinValueValidator(0), MaxValueValidator(100)]
        )
    
    


