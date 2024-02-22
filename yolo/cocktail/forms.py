# dans le fichier forms.py de l'application
from django import forms
from .models import Cocktail


class CocktailForm(forms.ModelForm):
    class Meta:
        model = Cocktail
        fields = ['name', 'ingredients', 'alcoholic',
                  'instructions']  # champs gérés par le formulaire
