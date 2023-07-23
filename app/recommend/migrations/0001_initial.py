# Generated by Django 4.2 on 2023-07-22 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeGraph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_selected', models.IntegerField(default=0)),
                ('dish1', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='DishTable1', to='recipe.dish')),
                ('dish2', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='DishTable2', to='recipe.dish')),
            ],
        ),
    ]