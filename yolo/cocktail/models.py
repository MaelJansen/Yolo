from django.db import models
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.fields import RichTextField
from wagtail.search import index


class Cocktail(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="cocktail_images", blank=True)
    ingredients = models.JSONField(default=list)
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


class CocktailPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'CocktailPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class CocktailPage(Page):
    strDrink = models.CharField(max_length=200)
    strDrinkThumb = models.CharField(
        max_length=255, default="https://img.freepik.com/vecteurs-premium/vecteur-icone-image-par-defaut-page-image-manquante-pour-conception-site-web-application-mobile-aucune-photo-disponible_87543-11093.jpg", blank=True, null=True)
    idDrink = models.CharField(max_length=200)
    ingredients = models.JSONField(default=list, blank=True, null=True)
    strAlcoholic = models.CharField(max_length=50, default="Alcoholic")
    strInstructions = models.TextField(default="")

    tags = ClusterTaggableManager(through=CocktailPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("strDrink"),
        FieldPanel("strDrinkThumb"),
        FieldPanel("idDrink"),
        FieldPanel("ingredients"),
        FieldPanel("strAlcoholic"),
        FieldPanel("strInstructions"),
        FieldPanel("tags")
    ]

    search_auto_update = False


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


class CocktailTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        cocktailpages = CocktailPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['cocktailpages'] = cocktailpages
        return context
