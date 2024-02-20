from django.shortcuts import render
from .models import Cocktail

def liste_cocktail(request):
    Cocktail.fetch_and_create()
    cocktail = Cocktail.objects.all()
    return render(request, 'liste_cocktail.html', {'cocktails': cocktail})

