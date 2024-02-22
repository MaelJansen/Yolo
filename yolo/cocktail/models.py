from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.search import index

class Cocktail(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="cocktail_images", blank=True, null=True)
    ingredients = models.JSONField(default={"strIngredient1": "water", "strIngredient2": "salt"})
    alcoholic = models.CharField(max_length=50, default="Alcoholic")
    instructions = models.TextField(default="")

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
        FieldPanel("ingredients"),
        FieldPanel("alcoholic"),
        FieldPanel("instructions")
    ]

    def __str__(self) -> str:
        return self.name


class CocktailPage(Page):
    strDrink = models.CharField(max_length=200)
    strDrinkThumb = models.CharField(max_length=255, default="https://img.freepik.com/vecteurs-premium/vecteur-icone-image-par-defaut-page-image-manquante-pour-conception-site-web-application-mobile-aucune-photo-disponible_87543-11093.jpg", blank=True, null=True)
    idDrink = models.CharField(max_length=200)
    ingredients = models.JSONField(default=list)
    strAlcoholic = models.CharField(max_length=50, default="Alcoholic")
    strInstructions = models.TextField(default="")

    content_panels = Page.content_panels + [
        FieldPanel("strDrink"),
        FieldPanel("strDrinkThumb"),
        FieldPanel("idDrink"),
        FieldPanel("ingredients"),
        FieldPanel("strAlcoholic"),
        FieldPanel("strInstructions")
    ]

    search_auto_update = False

    search_fields = Page.search_fields + [
        index.SearchField("strDrink"),
        index.SearchField("idDrink"),
    ]


class CocktailIndexPage(Page):
    def get_cocktails(self):
        return (
            CocktailPage.objects.live()
        )

    def paginate(self, request, *args):
        page = request.GET.get("page")
        paginator = Paginator(self.get_cocktails(), 6)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super().get_context(request)
        cocktails = self.paginate(request)
        context["Cocktails"] = cocktails
        return context
