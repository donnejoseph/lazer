from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from django.template.response import TemplateResponse
from shop.models import ProductPage, CategoryPage
from django.db import models


class HomePage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def serve(self, request):
        context = self.get_context(request)
        context['request'] = request  # Передаём request в контекст
        return TemplateResponse(request, self.get_template(request), context)

    def get_context(self, request):
        context = super().get_context(request)
        context['best_sellers'] = ProductPage.objects.filter(is_promotional=True)[:6]
        context['categories'] = CategoryPage.objects.live().public()
        context['home_page'] = self
        context['catalog_page'] = CatalogPage.objects.first() or None
        context['opt_page'] = OptPage.objects.first() or None
        context['news_page'] = NewsPage.objects.first() or None
        context['about_page'] = AboutPage.objects.first() or None
        return context

    class Meta:
        verbose_name = "Главная страница"


class CatalogPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def serve(self, request):
        return self.render(request, context_overrides={'request': request})

    def get_context(self, request):
        context = super().get_context(request)

        categories = CategoryPage.objects.filter(
            id__in=[1689, 1690, 3293, 1691, 1693, 1694]
        ).prefetch_related('products')
        category_map = {category.id: category for category in categories}

        context.update({
            'best_sellers': ProductPage.objects.filter(is_promotional=True)[:6],
            'manej': category_map.get(1689).products.all() if 1689 in category_map else [],
            'pazly': category_map.get(1690).products.all() if 1690 in category_map else [],
            'podstavki': category_map.get(3293).products.all() if 3293 in category_map else [],
            'panno': category_map.get(1691).products.all() if 1691 in category_map else [],
            'upakovka': category_map.get(1693).products.all() if 1693 in category_map else [],
            'rukodelie': category_map.get(1694).products.all() if 1694 in category_map else [],
            'home_page': HomePage.objects.first(),
            'catalog_page': self,
            'opt_page': OptPage.objects.first(),
            'news_page': NewsPage.objects.first(),
            'about_page': AboutPage.objects.first(),
        })
        return context

    class Meta:
        verbose_name = "Каталог"


class OptPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def serve(self, request):
        return self.render(request, context_overrides={'request': request})

    def get_context(self, request):
        context = super().get_context(request)
        context.update({
            'best_sellers': ProductPage.objects.filter(is_promotional=True)[:10],
            'home_page': HomePage.objects.first(),
            'catalog_page': CatalogPage.objects.first(),
            'opt_page': self,
            'news_page': NewsPage.objects.first(),
            'about_page': AboutPage.objects.first(),
        })
        return context

    class Meta:
        verbose_name = "Оптовикам"


class NewsPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def serve(self, request):
        return self.render(request, context_overrides={'request': request})

    def get_context(self, request):
        context = super().get_context(request)
        context.update({
            'best_sellers': ProductPage.objects.filter(is_promotional=True)[:16],
            'home_page': HomePage.objects.first(),
            'catalog_page': CatalogPage.objects.first(),
            'opt_page': OptPage.objects.first(),
            'news_page': self,
            'about_page': AboutPage.objects.first(),
        })
        return context

    class Meta:
        verbose_name = "Новости"


class AboutPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def serve(self, request):
        return self.render(request, context_overrides={'request': request})

    def get_context(self, request):
        context = super().get_context(request)
        context.update({
            'home_page': HomePage.objects.first(),
            'catalog_page': CatalogPage.objects.first(),
            'opt_page': OptPage.objects.first(),
            'news_page': NewsPage.objects.first(),
            'about_page': self,
        })
        return context

    class Meta:
        verbose_name = "Контакты"


@register_snippet
class StocksFormSnippet(models.Model):
    """
    Snippet для переиспользуемой формы.
    """
    title = models.CharField(max_length=255, help_text="Название формы для админки")
    success_message = RichTextField(blank=True, help_text="Сообщение, которое будет отображено после отправки.")

    panels = [
        FieldPanel('title'),
        FieldPanel('success_message'),
    ]

    def __str__(self):
        return self.title


class StocksFormSubmission(models.Model):
    """
    Модель для сохранения отправленных данных формы.
    """
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    agreement = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.submitted_at}"
