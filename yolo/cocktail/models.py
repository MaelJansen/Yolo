from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class Cocktail(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="cocktail_images", blank=True)
    ingredients = models.JSONField(default=list)
    alcoholic = models.CharField(max_length=50, default="Alcoholic")

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
        FieldPanel("ingredients"),
        FieldPanel("alcoholic")
    ]

    def __str__(self) -> str:
        return self.name


class CocktailPage(Page):
    strDrink = models.CharField(max_length=200)
    strDrinkThumb = models.CharField(max_length=255)
    idDrink = models.CharField(max_length=200)
    ingredients = models.JSONField(default=list)
    strAlcoholic = models.CharField(max_length=50, default="Alcoholic")

    content_panels = Page.content_panels + [
        FieldPanel("strDrink"),
        FieldPanel("strDrinkThumb"),
        FieldPanel("idDrink"),
        FieldPanel("ingredients"),
        FieldPanel("strAlcoholic")
    ]

    search_auto_update = False


class CocktailIndexPage(Page):
    def get_cocktails(self):
        return (
            CocktailPage.objects.live()
        )

    def paginate(self, request, *args):
        page = request.GET.get("page")
        paginator = Paginator(self.get_cocktails(), 3)
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
        print("THIS IS THE CONTEXT", context)
        return context
