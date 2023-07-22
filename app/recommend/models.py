from django.db import models
from app.recipe.models import Dish

# Create your models here.
class RecipeGraph(models.Model):
    dish1 = models.ForeignKey(
            Dish,
            default=-1,
            related_name="DishTable1",
            on_delete=models.CASCADE,
        )
    dish2 = models.ForeignKey(
            Dish,
            default=-1,
            related_name="DishTable2",
            on_delete=models.CASCADE,
        )
    num_selected = models.IntegerField(default=0)