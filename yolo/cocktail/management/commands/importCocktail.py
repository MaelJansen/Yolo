import csv
from django.core.management.base import BaseCommand
from wagtail.models import Page
from ...models import CocktailPage, CocktailIndexPage
import json
import requests


class Command(BaseCommand):

    def handle(self, *args, **options):
        CocktailPage.objects.all().delete()
        CocktailIndexPage.objects.all().delete()
        
        # Obtenez la page d'accueil
        home = Page.objects.get(id=3)
        
        # Créez la page d'index des cocktails
        cocktails_index_page = CocktailIndexPage(title="Cocktails")
        home.add_child(instance=cocktails_index_page)
        cocktails_index_page.save_revision().publish()

        # Obtenez les données JSON de l'API
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Cocktail')
        data = response.json()
        
        # Assurez-vous que la clé "drinks" existe dans les données JSON
        drinks = data.get('drinks', [])
        
        # Parcourez chaque cocktail et créez une page CocktailPage pour chaque
        for drink in drinks:
            strDrink = drink.get('strDrink', '')
            strDrinkThumb = drink.get('strDrinkThumb', '')
            idDrink = drink.get('idDrink', '')
                
            cocktail_page = CocktailPage(
                title=strDrink,
                strDrink=strDrink,
                strDrinkThumb=strDrinkThumb,
                idDrink=idDrink
            )
            cocktails_index_page.add_child(instance=cocktail_page)
            cocktail_page.save_revision().publish()
            print("Published cocktail page " + strDrink)
