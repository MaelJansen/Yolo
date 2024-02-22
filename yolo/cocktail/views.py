from django.shortcuts import get_object_or_404, render
from .models import Cocktail, CocktailPage
from rest_framework import permissions, viewsets, status, generics, serializers
from .serializers import CocktailSerializer
from django.views.decorators.csrf import csrf_protect
from .forms import CocktailForm
from rest_framework.decorators import api_view
from rest_framework.response import Response

import random
from django.shortcuts import render, redirect
from django.db import models
from .forms import CocktailForm
from .models import CocktailPage, CocktailIndexPage
from django.views.decorators.csrf import csrf_protect


def liste_cocktail(request):
    Cocktail.fetch_and_create()
    cocktail = Cocktail.objects.all()

    return render(request, 'liste_cocktail.html', {'cocktails': cocktail})


class CocktailViewSet(viewsets.ModelViewSet):
    queryset = CocktailPage.objects.all().order_by('id')
    serializer_class = CocktailSerializer
    permission_classes = [permissions.IsAuthenticated]


class CocktailDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = CocktailPage.objects.all()
    serializer_class = CocktailSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_cocktail': '/',
        'Search by Category': '/?category=category_name',
        'Search by Subcategory': '/?subcategory=category_name',
        'Add': '/add',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }

    return Response(api_urls)


@api_view(['POST'])
def add_cocktail(request):
    cocktail = CocktailSerializer(data=request.data)

    # validating for already existing data
    if Cocktail.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if cocktail.is_valid():
        cocktail.save()
        return Response(cocktail.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_cocktail(request, pk):
    cocktail = CocktailPage.objects.get(pk=pk)
    data = CocktailSerializer(instance=cocktail, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_cocktail(request, pk):
    cocktail = get_object_or_404(CocktailPage, pk=pk)
    cocktail.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

# route /cocktails/add


@csrf_protect
def creer_cocktail(request):
    if request.method == 'POST':
        # Si le formulaire est soumis, instanciez le formulaire avec les données de la requête
        form = CocktailForm(request.POST)

        # Vérifiez si le formulaire est valide
        if form.is_valid():
            # Enregistrez l'objet Article dans la base de données
            cocktail = form.save()
            name = form.cleaned_data.get('name')
            ingredients = form.cleaned_data.get('ingredients')
            # enlever le premier et le dernier caractère de la chaine de caractère
            print(type(ingredients))
         #    ingredients = ingredients[1:-1]
         #    ingredients = ingredients.replace('"', "")
         #    ingredients = ingredients.replace(": ", ", ")
            ingredients = ingredients.values()
            ingredients = list(ingredients)
            # concatenation des strings de la liste ingredients avec un virule dans une chaine de caractères
            ingredients = ', '.join(ingredients)
            alcoholic = form.cleaned_data.get('alcoholic')
            instructions = form.cleaned_data.get('instructions')

            cocktail_page = CocktailPage(
                title=name,
                strDrink=name,
                ingredients=ingredients,
                strAlcoholic=alcoholic,
                strInstructions=instructions,
                idDrink=random.randint(180, 1000000)
            )

            cocktail_index_page = CocktailIndexPage.objects.first()
            cocktail_index_page.add_child(instance=cocktail_page)
            cocktail_page.save_revision().publish()

            # Redirection vers la liste des articles après l'enregistrement
            return redirect(f'/cocktails/{name}')

    else:
        # Si la requête est GET, créez une instance du formulaire vide
        form = CocktailForm()

    # template html de la page du formulaire
    return render(request, './cocktail/form_cocktail_add.html', {'form': form})
