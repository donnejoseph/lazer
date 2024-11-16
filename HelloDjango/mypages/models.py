# mypages/models.py
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from shop.models import ProductPage, CategoryPage


class HomePage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['best_sellers'] = ProductPage.objects.filter(is_promotional=True)[:6]
        context['home_page'] = self
        context['catalog_page'] = CatalogPage.objects.first() or None
        context['opt_page'] = OptPage.objects.first() or None
        context['news_page'] = NewsPage.objects.first() or None
        context['about_page'] = AboutPage.objects.first() or None
        return context


class CatalogPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['best_sellers'] = ProductPage.objects.filter(is_promotional=True)[:6]
        context['manej'] = ProductPage.objects.filter(category=CategoryPage.objects.get(id=5))
        context['home_page'] = HomePage.objects.first()  # Получаем страницу главной
        context['catalog_page'] = self
        context['opt_page'] = OptPage.objects.first()
        context['news_page'] = NewsPage.objects.first() or None
        context['about_page'] = AboutPage.objects.first()  # Получаем страницу "О нас"
        return context


class OptPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['best_sellers'] = ProductPage.objects.filter(is_promotional=True)[:6]
        context['home_page'] = HomePage.objects.first()  # Получаем страницу главной
        context['catalog_page'] = CatalogPage.objects.first()  # Получаем страницу каталога
        context['opt_page'] = self
        context['news_page'] = NewsPage.objects.first() or None
        context['about_page'] = AboutPage.objects.first()  # Получаем страницу "О нас"
        return context


class NewsPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['home_page'] = HomePage.objects.first()  # Получаем страницу главной
        context['catalog_page'] = CatalogPage.objects.first()  # Получаем страницу каталога
        context['opt_page'] = OptPage.objects.first()
        context['news_page'] = self
        context['about_page'] = AboutPage.objects.first()  # Получаем страницу "О нас"
        return context


class AboutPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['home_page'] = HomePage.objects.first()  # Получаем страницу главной
        context['catalog_page'] = CatalogPage.objects.first()  # Получаем страницу каталога
        context['opt_page'] = OptPage.objects.first()
        context['news_page'] = NewsPage.objects.first() or None
        context['about_page'] = self
        return context
