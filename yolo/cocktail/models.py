from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

class CocktailIndexPage(Page):
    pass

class CocktailPage(Page):
    parent_page_types = ["cocktail.CocktailIndexPage"]
    strDrink = models.CharField(max_length=200)
    strDrinkThumb = models.CharField(max_length=255)
    idDrink = models.CharField(max_length=200)

    content_panels = Page.content_panels + [
        FieldPanel("strDrink"),
        FieldPanel("strDrinkThumb"),
        FieldPanel("idDrink"),
    ]
    
    search_auto_update = False
