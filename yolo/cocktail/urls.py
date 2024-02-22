
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('cocktails/add/', views.add_cocktail, name='add'),
    path('cocktails/update/<str:pk>/', views.update_cocktail, name='update'),
    path('cocktails/delete/<str:pk>/', views.delete_cocktail, name='delete'),
    path('cocktails/',
         views.CocktailViewSet.as_view({'get': 'list'}), name='all_cocktail'),
    path('cocktails/<str:pk>/', views.CocktailDetailViewSet.as_view(),
         name='detail_cocktail'),
]
