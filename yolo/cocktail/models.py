from django.db import models
import requests
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel

class Cocktail(models.Model):
    strDrink = models.CharField(max_length=200)
    strDrinkThumb = models.CharField(max_length=255)
    idDrink = models.CharField(max_length=200)

    def __str__(self):
        return self.titre
    
    content_panels = Page.content_panels + [
        FieldPanel('strDrink'),
        FieldPanel('strDrinkThumb'),
        FieldPanel('idDrink'),
    ]

    @classmethod
    def fetch_and_create(cls):
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Cocktail')
        if response.status_code == 200:
            data = response.json()
            drinks = data.get('drinks', [])
            for drink in drinks:
                cls.objects.create(
                    strDrink=drink.get('strDrink', ''),
                    strDrinkThumb=drink.get('strDrinkThumb', ''),
                    idDrink=drink.get('idDrink', '')
                )   