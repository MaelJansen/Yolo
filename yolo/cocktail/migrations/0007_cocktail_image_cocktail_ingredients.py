# Generated by Django 5.0.2 on 2024-02-21 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktail', '0006_cocktailpage_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='cocktail',
            name='image',
            field=models.ImageField(blank=True, upload_to='cocktail_images'),
        ),
        migrations.AddField(
            model_name='cocktail',
            name='ingredients',
            field=models.JSONField(default=list),
        ),
    ]
