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
        response = requests.get(
            'https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Cocktail')
        data = response.json()

        # Assurez-vous que la clé "drinks" existe dans les données JSON
        drinks = data.get('drinks', [])

        # Parcourez chaque cocktail et créez une page CocktailPage pour chaque
        for drink in drinks:
            idDrink = drink.get('idDrink', '')

            # Faites une autre requête pour obtenir les détails du cocktail
            details_response = requests.get(
                f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={idDrink}')
            details_data = details_response.json()
            cocktail_details = details_data.get('drinks', [])[0]

            strDrink = cocktail_details.get('strDrink', '')
            strDrinkThumb = cocktail_details.get('strDrinkThumb', '')
            strAlcoholic = cocktail_details.get('strAlcoholic', '')
            strInstructions = cocktail_details.get('strInstructions', '')
            ingredients = []

            # Get the ingredients
            for i in range(1, 16):
                ingredient = cocktail_details.get(f'strIngredient{i}', '')
                if ingredient:
                    ingredients.append(f'{ingredient}')

            cocktail_page = CocktailPage(
                title=strDrink,
                strDrink=strDrink,
                strDrinkThumb=strDrinkThumb,
                idDrink=idDrink,
                strAlcoholic=strAlcoholic,
                ingredients=ingredients,
                strInstructions=strInstructions

            )
            cocktails_index_page.add_child(instance=cocktail_page)
            cocktail_page.save_revision().publish()
            print("Published cocktail page " + strDrink)
