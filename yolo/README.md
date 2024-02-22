# Yolo : application d'indexage de cocktails

Auteurs :

- Jules Dupont
- Alex Gimbeau
- Maël Jansen
- Damien Levrault
- Clément Tomera

## Dépendances

- Django>=4.2,<5.1
- wagtail>=6.0,<6.1
- `pip install django-allauth`
- `pip install djangorestframework`

## Fonctionnalités

### Utilisateur

- création de compte
- connextion / déconnexion

### Cocktails

- Lister des cocktails
- Filter les cocktails par tags (ingrédients)
- Voir les détails d'un cocktail
- Ajouter un cocktail

### Avancé

- commande pour remplir la base :
  `python manage.py importCocktail`
- paramétrage de la galerie d'images dans Wagtail par les admin

### API REST

- Créer un cocktail
- Mettre à jour les infos d'un cocktail
- Lister les cocktails en base
- Suppimer des cocktails
