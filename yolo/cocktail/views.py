from django.shortcuts import get_object_or_404, render
from .models import Cocktail
from rest_framework import permissions, viewsets, status, generics, serializers
from .serializers import CocktailSerializer
from django.views.decorators.csrf import csrf_protect
from .forms import CocktailForm
from rest_framework.decorators import api_view
from rest_framework.response import Response


def liste_cocktail(request):
    Cocktail.fetch_and_create()
    cocktail = Cocktail.objects.all()
    
    return render(request, 'liste_cocktail.html', {'cocktails': cocktail})

class CocktailViewSet(viewsets.ModelViewSet):
    queryset = Cocktail.objects.all().order_by('idDrink')
    serializer_class = CocktailSerializer
    permission_classes = [permissions.IsAuthenticated]

class CocktailDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cocktail.objects.all()
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
    cocktail = Cocktail.objects.get(pk=pk)
    data = CocktailSerializer(instance=cocktail, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def delete_cocktail(request, pk):
    cocktail = get_object_or_404(Cocktail, pk=pk)
    cocktail.delete()
    return Response(status=status.HTTP_202_ACCEPTED)