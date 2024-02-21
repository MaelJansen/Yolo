from django.db.models import fields
from rest_framework import serializers
from .models import Cocktail
 
class CocktailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cocktail
        fields = ('id', 'strDrink', 'strDrinkThumb', 'idDrink')