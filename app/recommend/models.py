from django.db import models
from recipe.models import Dish

# Create your models here.
class RecipeGraph(models.Model):
    id1_dish = models.ForeignKey(
            Dish,
            related_name="DishTable1",
            on_delete=models.CASCADE,
        )
    id2_dish = models.ForeignKey(
            Dish,
            related_name="DishTable2",
            on_delete=models.CASCADE,
        )
    num_selected = models.IntegerField(default=0)