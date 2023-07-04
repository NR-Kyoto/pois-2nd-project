# Generated by Django 4.1 on 2023-06-27 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0003_delete_recipe_menudetail_dish_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookingtool',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='menudetail',
            name='dish_id',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='recipe.dish'),
        ),
    ]
