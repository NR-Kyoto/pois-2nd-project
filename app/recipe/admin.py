from django.contrib import admin
from .models import Dish, Menu, MenuDetail, CookingTool

# Register your models here.

admin.site.register(Dish)
admin.site.register(Menu)
admin.site.register(MenuDetail)
admin.site.register(CookingTool)