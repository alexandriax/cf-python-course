# Generated by Django 4.2.20 on 2025-03-30 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0002_remove_ingredient_recipe_alter_ingredient_name'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(to='ingredients.ingredient'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(blank=True, editable=False, max_length=20),
        ),
    ]
