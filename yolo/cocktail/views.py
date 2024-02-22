# dans views.py
import random
from django.shortcuts import render, redirect
from django.db import models
from .forms import CockatilForm
from .models import CocktailPage, CocktailIndexPage
from django.views.decorators.csrf import csrf_protect

# route /cocktails/add
@csrf_protect
def creer_article(request):
       if request.method == 'POST':
           # Si le formulaire est soumis, instanciez le formulaire avec les données de la requête
           form = CockatilForm(request.POST)

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

               return redirect(f'/cocktails/{name}') # Redirection vers la liste des articles après l'enregistrement

       else:
           # Si la requête est GET, créez une instance du formulaire vide
           form = CockatilForm()

       return render(request, './cocktail/form_cocktail_add.html', {'form': form}) # template html de la page du formulaire 
