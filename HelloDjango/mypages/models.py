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
        context['categories'] = CategoryPage.objects.live().public()
        return context

    class Meta:
        verbose_name = "Главная страница"


class CatalogPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Используем `prefetch_related` и `select_related` для оптимизации запросов
        categories = CategoryPage.objects.filter(id__in=[1689, 1690, 3293, 1691, 1693, 1694]).prefetch_related('products')
        category_map = {category.id: category for category in categories}

        # Получаем продукты для каждой категории
        context['best_sellers'] = ProductPage.objects.filter(is_promotional=True)[:6]
        context['manej'] = category_map.get(1689).products.all() if 1689 in category_map else []
        context['pazly'] = category_map.get(1690).products.all() if 1690 in category_map else []
        context['podstavki'] = category_map.get(3293).products.all() if 3293 in category_map else []
        context['panno'] = category_map.get(1691).products.all() if 1691 in category_map else []
        context['upakovka'] = category_map.get(1693).products.all() if 1693 in category_map else []
        context['rukodelie'] = category_map.get(1694).products.all() if 1694 in category_map else []

        # Заранее загружаем страницы для меню
        context['home_page'] = HomePage.objects.first()
        context['catalog_page'] = self
        context['opt_page'] = OptPage.objects.first()
        context['news_page'] = NewsPage.objects.first()
        context['about_page'] = AboutPage.objects.first()

        return context

    class Meta:
        verbose_name = "Каталог"


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

    class Meta:
        verbose_name = "Оптовикам"


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

    class Meta:
        verbose_name = "Новости"


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

    class Meta:
        verbose_name = "Контакты"
