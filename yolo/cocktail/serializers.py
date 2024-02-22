from django.db.models import fields
from rest_framework import serializers
from .models import CocktailPage
 
class CocktailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocktailPage
        fields = ('id', 'strDrink', 'strDrinkThumb', 'idDrink')