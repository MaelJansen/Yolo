from django import forms
from .models import CocktailPage

class CocktailForm(forms.ModelForm):
    class Meta:
        model = CocktailPage
        fields = ['id', 'strDrink', 'strDrinkThumb', 'idDrink']