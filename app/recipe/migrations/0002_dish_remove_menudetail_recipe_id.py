# Generated by Django 4.1 on 2023-06-27 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('dish_id', models.AutoField(primary_key=True, serialize=False)),
                ('dish_name', models.CharField(max_length=50)),
                ('manual', models.JSONField()),
            ],
        ),
        migrations.RemoveField(
            model_name='menudetail',
            name='recipe_id',
        ),
    ]
