# Generated by Django 5.0.2 on 2024-02-22 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktail', '0014_alter_cocktail_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cocktailpage',
            name='strDrinkThumb',
            field=models.CharField(default='https://img.freepik.com/vecteurs-premium/vecteur-icone-image-par-defaut-page-image-manquante-pour-conception-site-web-application-mobile-aucune-photo-disponible_87543-11093.jpg', max_length=255),
        ),
    ]
